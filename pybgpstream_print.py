#!/usr/bin/env python
import argparse
import datetime

import pybgpstream

filter_start_date_time_obj = None


def _check_elem(elem, list_of_auth_as):
    pref = elem.fields["prefix"]
    aspath = elem.fields["as-path"]
    asorin = aspath.split(" ")[-1]
    return pref, aspath, asorin, asorin not in list_of_auth_as


def generate_streams(list_of_prefix, list_of_auth_as, interval, collectors):
    global filter_start_date_time_obj

    filter_end_date_time_obj = filter_start_date_time_obj + datetime.timedelta(minutes=interval)
    from_time = filter_start_date_time_obj.strftime("%Y-%m-%d %H:%M:%S UTC")
    until_time = filter_end_date_time_obj.strftime("%Y-%m-%d %H:%M:%S UTC")

    print("currently reviewing from {} to {}".format(from_time, until_time), end="\n", flush=True)

    stream = pybgpstream.BGPStream(
        from_time=from_time,
        until_time=until_time,
        collectors=collectors,  # http://www.routeviews.org/routeviews/index.php/collectors/
        record_type="updates",
    )
    for prefix in list_of_prefix:
        stream.add_filter("prefix-more", prefix)

    print("Got Stream", end="\n", flush=True)

    for elem in stream:
        try:
            pref, aspath, asorin, is_hijack = _check_elem(elem, list_of_auth_as)
            print(f"Expected Announcement found: {pref} - {aspath} - {asorin}", flush=True)
            if is_hijack:
                print(f"*** Potential Hijack ***\n prefix {pref} by as {asorin}")
                print(elem)

        except AttributeError:
            # withdrawals arrive as update|W with no fields
            print(elem, end="\n", flush=True)

        except KeyError as e:
            print(e)
            print(elem, end="\n", flush=True)

    filter_start_date_time_obj = filter_start_date_time_obj + datetime.timedelta(minutes=interval)


def search_streams(start_time, stop_time, list_of_auth_as, list_of_prefixes, interval, collectors):
    global filter_start_date_time_obj

    filter_start_date_time_obj = datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    finish_date_time_obj = datetime.datetime.strptime(stop_time, "%Y-%m-%d %H:%M:%S")

    print("looking from {} to {}".format(start_time, stop_time), end="\n", flush=True)

    while finish_date_time_obj > filter_start_date_time_obj:
        generate_streams(list_of_prefixes, list_of_auth_as, interval, collectors)


def main():
    parser = argparse.ArgumentParser(
        description="Detect BGP prefix hijacks by monitoring route announcements."
    )
    parser.add_argument(
        "--prefix",
        dest="prefixes",
        action="append",
        required=True,
        metavar="PREFIX",
        help="IP prefix to monitor (repeatable, e.g. --prefix 185.70.40.0/24)",
    )
    parser.add_argument(
        "--authorized-as",
        dest="authorized_as",
        action="append",
        required=True,
        metavar="ASN",
        help="AS number authorised to announce the prefix (repeatable)",
    )
    parser.add_argument(
        "--start",
        required=True,
        metavar="DATETIME",
        help='Start of the review window, e.g. "2020-09-29 16:00:00"',
    )
    parser.add_argument(
        "--stop",
        required=True,
        metavar="DATETIME",
        help='End of the review window, e.g. "2020-09-29 18:59:59"',
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=180,
        metavar="MINUTES",
        help="Stream chunk size in minutes (default: 180)",
    )
    parser.add_argument(
        "--collector",
        dest="collectors",
        action="append",
        default=None,
        metavar="COLLECTOR",
        help="BGP collector to query (repeatable, default: rrc00). "
        "See routeviews.org/routeviews/index.php/collectors/",
    )
    args = parser.parse_args()

    search_streams(
        start_time=args.start,
        stop_time=args.stop,
        list_of_auth_as=args.authorized_as,
        list_of_prefixes=args.prefixes,
        interval=args.interval,
        collectors=args.collectors or ["rrc00"],
    )


if __name__ == "__main__":
    main()
