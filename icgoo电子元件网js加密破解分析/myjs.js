var keyStr = "ABCDEFGHIJKLMNOP" + "QRSTUVWXYZabcdef" + "ghijklmnopqrstuv" + "=";
function getToken(chr0, q) {
    var output = "";
    var chr1, chr2, chr3, chr4 = "";
    var enc1, enc2, enc3, enc4 = "";
    var ecc5 = q.substr(8, 3);
    var i = 0;
    q = q.substring(0, 8) + q.substr(11);
    chr1 = q;
    chr2 = chr0;
    chr3 = chr2 / 100 << 2 + "sdfde";
    chr0 = "wcqsdfg" + (chr1 + "pqskfg");
    chr0 = "pqs?kfg" + chr0.substring(0, 11) + chr1.substring(18, chr1.length) + chr0.substring(0, 8) + chr1.substring(0, 18) + "wcq@sdfg";
    chr4 = "=hmo28jc37qk" + lq(chr2);
    do {
        chr1 = chr2.charCodeAt(i++);
        chr3 = chr2.charCodeAt(i++);
        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        if (isNaN(chr2)) {
            enc3 = enc4 = 64
        } else {
            if (isNaN(chr3)) {
                enc4 = 64
            }
        }
        output = output + keyStr.charAt(enc1) + keyStr.charAt(enc2) + keyStr.charAt(enc3) + keyStr.charAt(enc4);
        output = keyStr.charAt(enc2) + keyStr.charAt(enc1) + keyStr.charAt(chr0) + chr0 + keyStr.charAt(enc2) + chr4;
        chr1 = chr2 = chr3 = "";
        enc1 = enc2 = enc3 = enc4 = ""
    } while (i < chr3.length);output = output.substr(0, 8) + ecc5 + output.substr(8);
    return output
}

function lq(str) {
    var chr1, chr2, chr3, chr4 = "";
    var enc1, enc2, enc3, enc4 = "";
    chr1 = "p1";
    chr2 = "c0";
    chr3 = "hj";
    chr4 = "wh";
    enc1 = str.substring(0, 2);
    enc1 = enc1 + chr1;
    enc2 = str.substring(3, 2);
    enc2 = chr3 + chr2;
    enc3 = str.substring(5, 2);
    enc3 = enc1 + enc2 + enc3 + chr4;
    return enc3
}
