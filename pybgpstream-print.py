#!/usr/bin/env python
import pybgpstream
import datetime

global filter_start_date_time_obj
global filter_end_date_time_obj
global finish_date_time_obj


def generate_streams(list_of_prefix, list_of_auth_as, interval):
    global filter_start_date_time_obj
    global filter_end_date_time_obj

    filter_end_date_time_obj = filter_start_date_time_obj + datetime.timedelta(minutes=interval)
    from_time = filter_start_date_time_obj.strftime("%Y-%m-%d %H:%M:%S UTC")
    until_time = filter_end_date_time_obj.strftime("%Y-%m-%d %H:%M:%S UTC")

    print("currently reviewing from {} to {}".format(from_time, until_time), end="\n", flush=True)

    stream = pybgpstream.BGPStream(
        from_time=from_time,
        until_time=until_time,
        collectors=["rrc00"],  # http://www.routeviews.org/routeviews/index.php/collectors/
        record_type="updates",
    )
    for prefix in list_of_prefix:
        stream.add_filter("prefix-more", prefix)

    print("Got Stream", end="\n", flush=True)

    for elem in stream:
        try:
            pref = elem.fields['prefix']
            aspath = elem.fields['as-path']
            asorin = aspath.split(" ")[-1]
            print("Expected Announcement found: {} - {} - {}".format(pref, aspath, asorin), end="\n", flush=True)
            if asorin not in list_of_auth_as:
                print("*** Potential Hijack ***\n prefix {} by as {}".format(prefix, asorin))
                print(elem)

        except AttributeError:
            # withdrawls expected here update|W
            print(elem, end="\n", flush=True)

        except KeyError as e:
            print(e)
            print(elem, end="\n", flush=True)

    filter_start_date_time_obj = filter_start_date_time_obj + datetime.timedelta(minutes=interval)


def search_streams(start_time, stop_time, list_of_auth_as, list_of_prefixes, interval):
    global filter_start_date_time_obj
    global finish_date_time_obj

    filter_start_date_time_obj = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    finish_date_time_obj = datetime.datetime.strptime(stop_time, '%Y-%m-%d %H:%M:%S')

    print("looking from {} to {}".format(start_time, stop_time), end="\n", flush=True)

    while finish_date_time_obj > filter_start_date_time_obj:
        generate_streams(list_of_prefixes, list_of_auth_as, interval)


# http://bgpstream.com/event/251745 185.70.40.0/24 by AS62371 grabbed by 1221
these_prefixes = ['185.70.40.0/24']
these_as = ['62371']
search_streams(start_time="2020-09-29 16:00:00",
               stop_time="2020-09-29 18:59:59",
               list_of_auth_as=these_as, list_of_prefixes=these_prefixes, interval=180)


# http://bgpstream.com/event/251891 193.186.253.0/24 by AS61317 grabbed by 18229
these_prefixes = ['193.186.253.0/24']
these_as = ['62371']
search_streams(start_time="2020-09-30 17:00:00", stop_time="2020-09-30 19:59:59",
               list_of_auth_as=these_as, list_of_prefixes=these_prefixes, interval=180)
