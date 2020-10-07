# bgp_rogue 

> Uses docker and pybgpstream to search for rogue Autonomous system announcing defined prefixes

```sh
$ docker build -t bgprogue . && docker run bgprogue
```

## Usage

Modify the these_prefixes & these_as paramaters to your prefixes and AS.  Then update the time window to review and internval - I found running day intervals seemed to work well but YMMV.

## Example Run

![](bgp_rogue.fin.gif)

## License

GPL-3.0 License © [Adam H](https://github.com/incendiary)
