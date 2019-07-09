function get_umuuid(ua, ts){
    function w() {
        function c(w, v) {
            var r, y = 0;
            for (r = 0; r < v.length; r++)
                y |= k[r] << 8 * r;
            return w ^ y
        }

        var d = ua, f, k = [], n = 0;
        for (f = 0; f < d.length; f++) {
            var u = d.charCodeAt(f);
            k.unshift(u & 255);
            4 <= k.length && (n = c(n, k),
                k = [])
        }
        0 < k.length && (n = c(n, k));
        return n.toString(16)
    }

    function b() {
        for (var c = 1 * new Date, d = 0; c == 1 * new Date; )
            d++;
        return c.toString(16) + d.toString(16)
    }

    function q() {
        var c = (1080 * 1920).toString(16);
        return b() + "-" + Math.random().toString(16).replace(".", "") + "-" + w() + "-" + c + "-" + b()
    }


    p = {
        "Ha": "",
        "Ja": "",
        "l": "1334253443-" + toString(ts) + "-",
        "la": true
    }
    var a = p, b;

    var c = q()
        , d = new Date;
    d.setTime(d.getTime() + 157248E5);
    var f = "www.mafengwo.cn".match(/[a-z0-9][a-z0-9\-]+\.[a-z\.]{2,6}$/i);
    b = c
    return b
}