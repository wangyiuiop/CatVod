var Crypto = (function() {
    var crypto = window.crypto || window.msCrypto;
    
    function md5cycle(x, k) {
        var a = x[0], b = x[1], c = x[2], d = x[3];
        a = ff(a, b, c, d, k[0], 7, -680876936);
        d = ff(d, a, b, c, k[1], 12, -389564586);
        c = ff(c, d, a, b, k[2], 17, 606105819);
        b = ff(b, c, d, a, k[3], 22, -1044525330);
        a = ff(a, b, c, d, k[4], 7, -176418897);
        d = ff(d, a, b, c, k[5], 12, 1200080426);
        c = ff(c, d, a, b, k[6], 17, -1473231341);
        b = ff(b, c, d, a, k[7], 22, -45705983);
        a = ff(a, b, c, d, k[8], 7, 1770035416);
        d = ff(d, a, b, c, k[9], 12, -1958414417);
        c = ff(c, d, a, b, k[10], 17, -42063);
        b = ff(b, c, d, a, k[11], 22, -1990404162);
        a = ff(a, b, c, d, k[12], 7, 1804603682);
        d = ff(d, a, b, c, k[13], 12, -40341101);
        c = ff(c, d, a, b, k[14], 17, -1502002290);
        b = ff(b, c, d, a, k[15], 22, 1236535329);
        a = gg(a, b, c, d, k[1], 5, -165796510);
        d = gg(d, a, b, c, k[6], 9, -1069501632);
        c = gg(c, d, a, b, k[11], 14, 643717713);
        b = gg(b, c, d, a, k[0], 20, -373897302);
        a = gg(a, b, c, d, k[5], 5, -701558691);
        d = gg(d, a, b, c, k[10], 9, 38016083);
        c = gg(c, d, a, b, k[15], 14, -660478335);
        b = gg(b, c, d, a, k[4], 20, -405537848);
        a = gg(a, b, c, d, k[9], 5, 568446438);
        d = gg(d, a, b, c, k[14], 9, -1019803690);
        c = gg(c, d, a, b, k[3], 14, -187363961);
        b = gg(b, c, d, a, k[8], 20, 1163531501);
        a = gg(a, b, c, d, k[13], 5, -1444681467);
        d = gg(d, a, b, c, k[2], 9, -51403784);
        c = gg(c, d, a, b, k[7], 14, 1735328473);
        b = gg(b, c, d, a, k[12], 20, -1926607734);
        a = hh(a, b, c, d, k[5], 4, -378558);
        d = hh(d, a, b, c, k[8], 11, -2022574463);
        c = hh(c, d, a, b, k[11], 16, 1839030562);
        b = hh(b, c, d, a, k[14], 23, -35309556);
        a = hh(a, b, c, d, k[1], 4, -1530992060);
        d = hh(d, a, b, c, k[4], 11, 1272893353);
        c = hh(c, d, a, b, k[7], 16, -155497632);
        b = hh(b, c, d, a, k[10], 23, -1094730640);
        a = hh(a, b, c, d, k[13], 4, 681279174);
        d = hh(d, a, b, c, k[0], 11, -358537222);
        c = hh(c, d, a, b, k[3], 16, -722521979);
        b = hh(b, c, d, a, k[6], 23, 76029189);
        a = hh(a, b, c, d, k[9], 4, -640364487);
        d = hh(d, a, b, c, k[12], 11, -421815835);
        c = hh(c, d, a, b, k[15], 16, 530742520);
        b = hh(b, c, d, a, k[2], 23, -995338651);
        a = ii(a, b, c, d, k[0], 6, -198630844);
        d = ii(d, a, b, c, k[7], 10, 1126891415);
        c = ii(c, d, a, b, k[14], 15, -1416354905);
        b = ii(b, c, d, a, k[3], 21, -57434055);
        a = ii(a, b, c, d, k[10], 6, 1700485571);
        d = ii(d, a, b, c, k[1], 10, -1894986606);
        c = ii(c, d, a, b, k[8], 15, -1051523);
        b = ii(b, c, d, a, k[15], 21, -2054922799);
        a = ii(a, b, c, d, k[6], 6, 1873313359);
        d = ii(d, a, b, c, k[13], 10, -30611744);
        c = ii(c, d, a, b, k[4], 15, -1560198380);
        b = ii(b, c, d, a, k[11], 21, 1309151649);
        a = ii(a, b, c, d, k[2], 6, -145523070);
        d = ii(d, a, b, c, k[9], 10, -1120210379);
        c = ii(c, d, a, b, k[0], 15, 718787259);
        b = ii(b, c, d, a, k[7], 21, -343485551);
        x[0] = add32(a, x[0]);
        x[1] = add32(b, x[1]);
        x[2] = add32(c, x[2]);
        x[3] = add32(d, x[3]);
    }
    
    function cmn(q, a, b, x, s, t) {
        a = add32(add32(a, q), add32(x, t));
        return add32((a << s) | (a >>> (32 - s)), b);
    }
    
    function ff(a, b, c, d, x, s, t) {
        return cmn((b & c) | ((~b) & d), a, b, x, s, t);
    }
    
    function gg(a, b, c, d, x, s, t) {
        return cmn((b & d) | (c & (~d)), a, b, x, s, t);
    }
    
    function hh(a, b, c, d, x, s, t) {
        return cmn(b ^ c ^ d, a, b, x, s, t);
    }
    
    function ii(a, b, c, d, x, s, t) {
        return cmn(c ^ (b | (~d)), a, b, x, s, t);
    }
    
    function md51(s) {
        var n = s.length,
            state = [1732584193, -271733879, -1732584194, 271733878],
            i;
        for (i = 64; i <= n; i += 64) {
            md5cycle(state, md5blk(s.substring(i - 64, i)));
        }
        s = s.substring(i - 64);
        var tail = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
        for (i = 0; i < s.length; i++)
            tail[i >> 2] |= s.charCodeAt(i) << ((i % 4) << 3);
        tail[i >> 2] |= 0x80 << ((i % 4) << 3);
        if (i > 55) {
            md5cycle(state, tail);
            for (i = 0; i < 16; i++) tail[i] = 0;
        }
        tail[14] = n * 8;
        md5cycle(state, tail);
        return state;
    }
    
    function md5blk(s) {
        var md5blks = [], i;
        for (i = 0; i < 64; i += 4) {
            md5blks[i >> 2] = s.charCodeAt(i) +
                (s.charCodeAt(i + 1) << 8) +
                (s.charCodeAt(i + 2) << 16) +
                (s.charCodeAt(i + 3) << 24);
        }
        return md5blks;
    }
    
    var hex_chr = '0123456789abcdef'.split('');
    
    function rhex(n) {
        var s = '', j = 0;
        for (; j < 4; j++)
            s += hex_chr[(n >> (j * 8 + 4)) & 0x0F] + hex_chr[(n >> (j * 8)) & 0x0F];
        return s;
    }
    
    function hex(x) {
        for (var i = 0; i < x.length; i++)
            x[i] = rhex(x[i]);
        return x.join('');
    }
    
    function add32(a, b) {
        return (a + b) & 0xFFFFFFFF;
    }
    
    function md5cycle2(x, k) {
        var a = x[0], b = x[1], c = x[2], d = x[3];
        a = ff(a, b, c, d, k[0], 7, -680876936);
        d = ff(d, a, b, c, k[1], 12, -389564586);
        c = ff(c, d, a, b, k[2], 17, 606105819);
        b = ff(b, c, d, a, k[3], 22, -1044525330);
        a = ff(a, b, c, d, k[4], 7, -176418897);
        d = ff(d, a, b, c, k[5], 12, 1200080426);
        c = ff(c, d, a, b, k[6], 17, -1473231341);
        b = ff(b, c, d, a, k[7], 22, -45705983);
        a = ff(a, b, c, d, k[8], 7, 1770035416);
        d = ff(d, a, b, c, k[9], 12, -1958414417);
        c = ff(c, d, a, b, k[10], 17, -42063);
        b = ff(b, c, d, a, k[11], 22, -1990404162);
        a = ff(a, b, c, d, k[12], 7, 1804603682);
        d = ff(d, a, b, c, k[13], 12, -40341101);
        c = ff(c, d, a, b, k[14], 17, -1502002290);
        b = ff(b, c, d, a, k[15], 22, 1236535329);
        a = gg(a, b, c, d, k[1], 5, -165796510);
        d = gg(d, a, b, c, k[6], 9, -1069501632);
        c = gg(c, d, a, b, k[11], 14, 643717713);
        b = gg(b, c, d, a, k[0], 20, -373897302);
        a = gg(a, b, c, d, k[5], 5, -701558691);
        d = gg(d, a, b, c, k[10], 9, 38016083);
        c = gg(c, d, a, b, k[15], 14, -660478335);
        b = gg(b, c, d, a, k[4], 20, -405537848);
        a = gg(a, b, c, d, k[9], 5, 568446438);
        d = gg(d, a, b, c, k[14], 9, -1019803690);
        c = gg(c, d, a, b, k[3], 14, -187363961);
        b = gg(b, c, d, a, k[8], 20, 1163531501);
        a = gg(a, b, c, d, k[13], 5, -1444681467);
        d = gg(d, a, b, c, k[2], 9, -51403784);
        c = gg(c, d, a, b, k[7], 14, 1735328473);
        b = gg(b, c, d, a, k[12], 20, -1926607734);
        a = hh(a, b, c, d, k[5], 4, -378558);
        d = hh(d, a, b, c, k[8], 11, -2022574463);
        c = hh(c, d, a, b, k[11], 16, 1839030562);
        b = hh(b, c, d, a, k[14], 23, -35309556);
        a = hh(a, b, c, d, k[1], 4, -1530992060);
        d = hh(d, a, b, c, k[4], 11, 1272893353);
        c = hh(c, d, a, b, k[7], 16, -155497632);
        b = hh(b, c, d, a, k[10], 23, -1094730640);
        a = hh(a, b, c, d, k[13], 4, 681279174);
        d = hh(d, a, b, c, k[0], 11, -358537222);
        c = hh(c, d, a, b, k[3], 16, -722521979);
        b = hh(b, c, d, a, k[6], 23, 76029189);
        a = hh(a, b, c, d, k[9], 4, -640364487);
        d = hh(d, a, b, c, k[12], 11, -421815835);
        c = hh(c, d, a, b, k[15], 16, 530742520);
        b = hh(b, c, d, a, k[2], 23, -995338651);
        a = ii(a, b, c, d, k[0], 6, -198630844);
        d = ii(d, a, b, c, k[7], 10, 1126891415);
        c = ii(c, d, a, b, k[14], 15, -1416354905);
        b = ii(b, c, d, a, k[3], 21, -57434055);
        a = ii(a, b, c, d, k[10], 6, 1700485571);
        d = ii(d, a, b, c, k[1], 10, -1894986606);
        c = ii(c, d, a, b, k[8], 15, -1051523);
        b = ii(b, c, d, a, k[15], 21, -2054922799);
        a = ii(a, b, c, d, k[6], 6, 1873313359);
        d = ii(d, a, b, c, k[13], 10, -30611744);
        c = ii(c, d, a, b, k[4], 15, -1560198380);
        b = ii(b, c, d, a, k[11], 21, 1309151649);
        a = ii(a, b, c, d, k[2], 6, -145523070);
        d = ii(d, a, b, c, k[9], 10, -1120210379);
        c = ii(c, d, a, b, k[0], 15, 718787259);
        b = ii(b, c, d, a, k[7], 21, -343485551);
        x[0] = add32(a, x[0]);
        x[1] = add32(b, x[1]);
        x[2] = add32(c, x[2]);
        x[3] = add32(d, x[3]);
    }
    
    function MD5(string) {
        return hex(md51(string));
    }
    
    function sha1(str) {
        var block, startIndex, i, t;
        var W = new Array(80);
        var H0 = 0x67452301, H1 = 0xEFCDAB89, H2 = 0x98BADCFE, H3 = 0x10325476, H4 = 0xC3D2E1F0;
        
        var a, b, c, d, e;
        var temp;
        
        block = str.length * 8;
        startIndex = 64 - (str.length + 8) % 64;
        if (startIndex === 64) startIndex = 0;
        
        str += "\x80";
        for (i = startIndex; i < 64; i++) str += "\x00";
        str += String.fromCharCode((block >>> 24) & 0xFF);
        str += String.fromCharCode((block >>> 16) & 0xFF);
        str += String.fromCharCode((block >>> 8) & 0xFF);
        str += String.fromCharCode(block & 0xFF);
        
        while (str.length >= 64) {
            block = new Array(16);
            for (i = 0; i < 16; i++) {
                block[i] = str.charCodeAt(i * 4) * 16777216 +
                           str.charCodeAt(i * 4 + 1) * 65536 +
                           str.charCodeAt(i * 4 + 2) * 256 +
                           str.charCodeAt(i * 4 + 3);
            }
            
            for (i = 0; i < 80; i++) {
                if (i < 16) {
                    W[i] = block[i];
                } else {
                    W[i] = rotL(W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16], 1);
                }
                t = rotL(a, 5) + (b & c | ~b & d) + e + W[i] + 1518500249;
                e = d; d = c; c = rotL(b, 30); b = a; a = t;
            }
            
            a = (a + H0) >>> 0;
            b = (b + H1) >>> 0;
            c = (c + H2) >>> 0;
            d = (d + H3) >>> 0;
            e = (e + H4) >>> 0;
            
            str = str.substring(16);
        }
        
        return wordToHex(a) + wordToHex(b) + wordToHex(c) + wordToHex(d) + wordToHex(e);
    }
    
    function rotL(n, s) {
        return (n << s) | (n >>> (32 - s));
    }
    
    function wordToHex(word) {
        var hex = "";
        for (var i = 0; i <= 3; i++) {
            hex += ((word >>> (i * 8)) & 255).toString(16);
        }
        return hex;
    }
    
    var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    var base64DecodeChars = new Array(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
    
    function base64encode(str) {
        var out, i, len;
        var c1, c2, c3;
        len = str.length;
        i = 0;
        out = "";
        while (i < len) {
            c1 = str.charCodeAt(i++) & 0xff;
            if (i === len) {
                out += base64EncodeChars.charAt(c1 >> 2);
                out += base64EncodeChars.charAt((c1 & 0x3) << 4);
                out += "==";
                break;
            }
            c2 = str.charCodeAt(i++);
            if (i === len) {
                out += base64EncodeChars.charAt(c1 >> 2);
                out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
                out += base64EncodeChars.charAt((c2 & 0xF) << 2);
                out += "=";
                break;
            }
            c3 = str.charCodeAt(i++);
            out += base64EncodeChars.charAt(c1 >> 2);
            out += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
            out += base64EncodeChars.charAt(c3 & 0x3F);
        }
        return out;
    }
    
    function base64decode(str) {
        var c1, c2, c3, c4;
        var i, len, out;
        len = str.length;
        i = 0;
        out = "";
        while (i < len) {
            do {
                c1 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while (i < len && c1 === -1);
            if (c1 === -1) break;
            do {
                c2 = base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while (i < len && c2 === -1);
            if (c2 === -1) break;
            out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));
            do {
                c3 = str.charCodeAt(i++) & 0xff;
                if (c3 === 61) return out;
                c3 = base64DecodeChars[c3];
            } while (i < len && c3 === -1);
            if (c3 === -1) break;
            out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));
            do {
                c4 = str.charCodeAt(i++) & 0xff;
                if (c4 === 61) return out;
                c4 = base64DecodeChars[c4];
            } while (i < len && c4 === -1);
            if (c4 === -1) break;
            out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
        }
        return out;
    }
    
    function utf16to8(str) {
        var out, i, len, c;
        out = "";
        len = str.length;
        for (i = 0; i < len; i++) {
            c = str.charCodeAt(i);
            if ((c >= 0x0001) && (c <= 0x007F)) {
                out += str.charAt(i);
            } else if (c > 0x07FF) {
                out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
                out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
                out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            } else {
                out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
                out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            }
        }
        return out;
    }
    
    function utf8to16(str) {
        var out, i, len, c;
        var char2, char3;
        out = "";
        len = str.length;
        i = 0;
        while (i < len) {
            c = str.charCodeAt(i++);
            switch (c >> 4) {
                case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
                    out += str.charAt(i - 1);
                    break;
                case 12: case 13:
                    char2 = str.charCodeAt(i++);
                    out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
                    break;
                case 14:
                    char2 = str.charCodeAt(i++);
                    char3 = str.charCodeAt(i++);
                    out += String.fromCharCode(((c & 0x0F) << 12) | ((char2 & 0x3F) << 6) | ((char3 & 0x3F) << 0));
                    break;
            }
        }
        return out;
    }
    
    function rc4(key, data) {
        var s = [], j = 0, x, res = '';
        for (var i = 0; i < 256; i++) {
            s[i] = i;
        }
        for (var i = 0; i < 256; i++) {
            j = (j + s[i] + key.charCodeAt(i % key.length)) % 256;
            x = s[i];
            s[i] = s[j];
            s[j] = x;
        }
        i = 0;
        j = 0;
        for (var k = 0; k < data.length; k++) {
            i = (i + 1) % 256;
            j = (j + s[i]) % 256;
            x = s[i];
            s[i] = s[j];
            s[j] = x;
            res += String.fromCharCode(data.charCodeAt(k) ^ s[(s[i] + s[j]) % 256]);
        }
        return res;
    }
    
    return {
        MD5: MD5,
        md5: MD5,
        sha1: sha1,
        SHA1: sha1,
        base64encode: base64encode,
        base64_decode: base64decode,
        base64decode: base64decode,
        utf16to8: utf16to8,
        utf8to16: utf8to16,
        rc4: rc4,
        createCipher: function(algorithm, key) {
            return {
                update: function(data) { return data; },
                final: function() { return ''; }
            };
        },
        createDecipher: function(algorithm, key) {
            return {
                update: function(data) { return data; },
                final: function() { return ''; }
            };
        },
        createHash: function(algorithm) {
            return {
                update: function(data) { return this; },
                digest: function() { return ''; }
            };
        },
        randomBytes: function(n) {
            var result = new Array(n);
            for (var i = 0; i < n; i++) {
                result[i] = Math.floor(Math.random() * 256);
            }
            return result;
        },
        pseudoRandomBytes: function(n) {
            return this.randomBytes(n);
        },
        randomUUID: function() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0;
                var v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }
    };
})();

var _ = {
    VERSION: '1.0.0',
    
    each: function(obj, iterate, context) {
        if (obj == null) return;
        if (Array.prototype.forEach && obj.forEach === Array.prototype.forEach) {
            obj.forEach(iterate, context);
        } else if (typeof obj.length === 'number') {
            for (var i = 0, l = obj.length; i < l; i++) {
                iterate.call(context, obj[i], i, obj);
            }
        } else {
            for (var key in obj) {
                if (obj.hasOwnProperty(key)) {
                    iterate.call(context, obj[key], key, obj);
                }
            }
        }
        return obj;
    },
    
    map: function(obj, iterate, context) {
        var results = [];
        if (obj == null) return results;
        if (Array.prototype.map && obj.map === Array.prototype.map) {
            return obj.map(iterate, context);
        }
        this.each(obj, function(value, index, list) {
            results.push(iterate.call(context, value, index, list));
        });
        return results;
    },
    
    values: function(obj) {
        var keys = Object.keys(obj);
        var result = [];
        for (var i = 0, l = keys.length; i < l; i++) {
            result.push(obj[keys[i]]);
        }
        return result;
    },
    
    keys: function(obj) {
        if (obj !== Object(obj)) throw new TypeError('Invalid object');
        var keys = [];
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) keys.push(key);
        }
        return keys;
    },
    
    isEmpty: function(obj) {
        if (obj == null) return true;
        if (Array.isArray(obj) || typeof obj === 'string') return obj.length === 0;
        for (var key in obj) {
            if (obj.hasOwnProperty(key)) return false;
        }
        return true;
    },
    
    isArray: Array.isArray || function(obj) {
        return Object.prototype.toString.call(obj) === '[object Array]';
    },
    
    isObject: function(obj) {
        var type = typeof obj;
        return type === 'function' || type === 'object' && !!obj;
    },
    
    isString: function(obj) {
        return Object.prototype.toString.call(obj) === '[object String]';
    },
    
    isNumber: function(obj) {
        return Object.prototype.toString.call(obj) === '[object Number]';
    },
    
    isFunction: function(obj) {
        return typeof obj === 'function';
    },
    
    isBoolean: function(obj) {
        return obj === true || obj === false || Object.prototype.toString.call(obj) === '[object Boolean]';
    },
    
    isUndefined: function(obj) {
        return obj === void 0;
    },
    
    isNull: function(obj) {
        return obj === null;
    },
    
    has: function(obj, path) {
        if (typeof path === 'string') path = path.split('.');
        for (var i = 0, l = path.length; i < l; i++) {
            if (obj == null) return false;
            obj = obj[path[i]];
        }
        return l > 0 || obj !== void 0;
    },
    
    get: function(obj, path, defaultValue) {
        if (typeof path === 'string') path = path.split('.');
        var value = obj;
        for (var i = 0, l = path.length; i < l; i++) {
            if (value == null) return defaultValue;
            value = value[path[i]];
        }
        return (l && value === void 0) ? defaultValue : value;
    },
    
    set: function(obj, path, value) {
        if (typeof path === 'string') path = path.split('.');
        var i = 0, l = path.length;
        while (i < l - 1) {
            if (obj[path[i]] == null) obj[path[i]] = {};
            obj = obj[path[i++]];
        }
        obj[path[i]] = value;
    },
    
    pick: function(obj) {
        var result = {};
        var keys = Array.prototype.concat.apply(Array.prototype, Array.prototype.slice.call(arguments, 1));
        for (var i = 0, l = keys.length; i < l; i++) {
            var key = keys[i];
            if (key in obj) result[key] = obj[key];
        }
        return result;
    },
    
    omit: function(obj) {
        var result = {};
        var keys = Array.prototype.concat.apply(Array.prototype, Array.prototype.slice.call(arguments, 1));
        for (var key in obj) {
            if (keys.indexOf(key) < 0) result[key] = obj[key];
        }
        return result;
    },
    
    clone: function(obj) {
        if (!_.isObject(obj)) return obj;
        return _.isArray(obj) ? obj.slice() : _.extend({}, obj);
    },
    
    extend: function(obj) {
        for (var i = 1, l = arguments.length; i < l; i++) {
            var source = arguments[i];
            if (source) {
                for (var prop in source) {
                    obj[prop] = source[prop];
                }
            }
        }
        return obj;
    },
    
    defaults: function(obj) {
        for (var i = 1, l = arguments.length; i < l; i++) {
            var source = arguments[i];
            if (source) {
                for (var prop in source) {
                    if (obj[prop] === void 0) obj[prop] = source[prop];
                }
            }
        }
        return obj;
    },
    
    uniqueId: (function() {
        var counter = 0;
        return function(prefix) {
            var id = ++counter;
            return prefix ? prefix + id : id;
        };
    })(),
    
    template: function(str, data) {
        var tmpl = 'var __p=[];' +
            'with(obj||{}){__p.push(\'' +
            str.replace(/\\/g, '\\\\')
               .replace(/'/g, "\\'")
               .replace(/<%=([\s\S]+?)%>/g, function(match, code) {
                   return "'," + code.replace(/\\'/g, "'") + ",'";
               })
               .replace(/<%([\s\S]+?)%>/g, function(match, code) {
                   return "');" + code.replace(/\\'/g, "'") + ";__p.push('";
               }) +
            "');}return __p.join('');";
        var func = new Function('obj', tmpl);
        return data ? func(data) : func;
    },
    
    filter: function(obj, predicate, context) {
        var results = [];
        if (obj == null) return results;
        predicate = predicate || _.identity;
        if (Array.prototype.filter && obj.filter === Array.prototype.filter) {
            return obj.filter(predicate, context);
        }
        this.each(obj, function(value, index, list) {
            if (predicate.call(context, value, index, list)) results.push(value);
        });
        return results;
    },
    
    find: function(obj, predicate, context) {
        if (obj == null) return undefined;
        if (typeof predicate === 'function') {
            for (var i = 0, l = obj.length; i < l; i++) {
                if (predicate.call(context, obj[i], i, obj)) return obj[i];
            }
        } else if (typeof obj === 'object') {
            for (var key in obj) {
                if (obj.hasOwnProperty(key) && predicate(obj[key], key, obj)) return obj[key];
            }
        }
        return undefined;
    },
    
    includes: function(obj, target, fromIndex) {
        if (obj == null) return false;
        if (Array.isArray(obj)) {
            return obj.indexOf(target, fromIndex) !== -1;
        }
        var len = obj.length;
        fromIndex = fromIndex == null ? 0 : fromIndex;
        if (fromIndex < 0) fromIndex = Math.max(len + fromIndex, 0);
        for (var i = fromIndex; i < len; i++) {
            if (obj[i] === target) return true;
        }
        return false;
    },
    
    indexOf: function(array, target, fromIndex) {
        if (array == null) return -1;
        var i = 0, l = array.length;
        if (typeof fromIndex === 'number') {
            i = fromIndex < 0 ? Math.max(0, l + fromIndex) : fromIndex;
        }
        for (; i < l; i++) {
            if (array[i] === target) return i;
        }
        return -1;
    },
    
    chunk: function(array, size) {
        size = Math.max(size, 0);
        var length = array == null ? 0 : array.length;
        if (!length || size < 1) return [];
        var result = [];
        for (var i = 0, l = Math.ceil(length / size); i < l; i++) {
            var start = i * size, end = Math.min(start + size, length);
            result.push(array.slice(start, end));
        }
        return result;
    },
    
    flatten: function(array, depth) {
        var output = [];
        for (var i = 0, l = array.length; i < l; i++) {
            var value = array[i];
            if (depth !== 0 && _.isArray(value)) {
                if (depth === 1) {
                    for (var j = 0, k = value.length; j < k; j++) {
                        output.push(value[j]);
                    }
                } else {
                    output = output.concat(_.flatten(value, depth - 1));
                }
            } else {
                output.push(value);
            }
        }
        return output;
    },
    
    uniq: function(array, isSorted, iteratee, context) {
        if (!_.isBoolean(isSorted)) {
            context = iteratee;
            iteratee = isSorted;
            isSorted = false;
        }
        if (iteratee != null) {
            iteratee = _.iteratee(iteratee);
        }
        var result = [];
        var seen = [];
        for (var i = 0, l = array.length; i < l; i++) {
            var value = array[i];
            var computed = iteratee ? iteratee(value, i, array) : value;
            if (isSorted) {
                if (!i || seen !== computed) {
                    result.push(value);
                    seen = computed;
                }
            } else if (iteratee) {
                if (seen.indexOf(computed) < 0) {
                    seen.push(computed);
                    result.push(value);
                }
            } else if (result.indexOf(value) < 0) {
                result.push(value);
            }
        }
        return result;
    },
    
    difference: function(array) {
        var rest = _.flatten(Array.prototype.slice.call(arguments, 1));
        return _.filter(array, function(value) {
            return rest.indexOf(value) < 0;
        });
    },
    
    intersection: function(array) {
        var rest = _.flatten(Array.prototype.slice.call(arguments, 1));
        return _.filter(_.uniq(array), function(value) {
            return rest.indexOf(value) >= 0;
        });
    },
    
    union: function() {
        return _.uniq(_.flatten(arguments));
    },
    
    sortBy: function(obj, iteratee, context) {
        var iterateeFn = _.isFunction(iteratee) ? iteratee : function(x) { return x[iteratee]; };
        return _.pluck(_.map(_.chunk(obj, 1), function(value, index, list) {
            return {
                value: value[0],
                criteria: iterateeFn.call(context, value[0], index, list)
            };
        }).sort(function(left, right) {
            var a = left.criteria, b = right.criteria;
            if (a !== b) {
                if (a > b || a === void 0) return 1;
                if (a < b || b === void 0) return -1;
            }
            return left.index - right.index;
        }), 'value');
    },
    
    groupBy: function(obj, iteratee, context) {
        var result = {};
        iteratee = _.isFunction(iteratee) ? iteratee : function(x) { return x[iteratee]; };
        _.each(obj, function(value, index) {
            var key = iteratee.call(context, value, index, obj);
            (result[key] || (result[key] = [])).push(value);
        });
        return result;
    },
    
    shuffle: function(obj) {
        var set = obj && obj.length === +obj.length ? obj : _.values(obj);
        var l = set.length;
        var indexed = [];
        for (var i = 0; i < l; i++) {
            var rand = _.random(i);
            indexed[i] = indexed[rand];
            indexed[rand] = set[i];
        }
        return indexed;
    },
    
    sample: function(obj, n, guard) {
        if (obj == null || n == null || guard) {
            if (obj && obj.length === +obj.length) return obj[_.random(obj.length - 1)];
            return undefined;
        }
        return _.shuffle(obj).slice(0, Math.max(0, n));
    },
    
    toArray: function(obj) {
        if (!obj) return [];
        if (_.isArray(obj)) return Array.prototype.slice.call(obj);
        if (obj.length === +obj.length) return _.map(obj, function(val) { return val; });
        return _.values(obj);
    },
    
    size: function(obj) {
        if (obj == null) return 0;
        return (obj.length === +obj.length) ? obj.length : _.keys(obj).length;
    },
    
    partition: function(obj, predicate, context) {
        var pass = [], fail = [];
        predicate = predicate || _.identity;
        _.each(obj, function(value, key, obj) {
            if (predicate.call(context, value, key, obj)) pass.push(value);
            else fail.push(value);
        });
        return [pass, fail];
    },
    
    compact: function(array) {
        return _.filter(array, _.identity);
    },
    
    first: function(array, n, guard) {
        if (array == null || array.length < 1) return undefined;
        if (n == null || guard) return array[0];
        if (n < 0) return [];
        return Array.prototype.slice.call(array, 0, n);
    },
    
    last: function(array, n, guard) {
        if (array == null || array.length < 1) return undefined;
        if (n == null || guard) return array[array.length - 1];
        if (n < 0) return [];
        return Array.prototype.slice.call(array, Math.max(array.length - n, 0));
    },
    
    identity: function(value) {
        return value;
    },
    
    constant: function(value) {
        return function() {
            return value;
        };
    },
    
    noop: function() {},
    
    property: function(path) {
        if (typeof path === 'string') return _.propertyOf({});
        return function(obj) {
            return obj == null ? undefined : obj[path];
        };
    },
    
    propertyOf: function(obj) {
        if (obj == null) return function() {};
        return function(path) {
            return _.get(obj, path);
        };
    },
    
    matcher: _.matches = function(attrs) {
        attrs = _.extend({}, attrs);
        return function(obj) {
            return _.isMatch(obj, attrs);
        };
    },
    
    isMatch: function(obj, attrs) {
        var keys = _.keys(attrs);
        var l = keys.length;
        if (obj == null) return !l;
        for (var i = 0; i < l; i++) {
            var key = keys[i];
            if (attrs[key] !== obj[key] || !(key in obj)) return false;
        }
        return true;
    },
    
    negate: function(predicate) {
        return function() {
            return !predicate.apply(this, arguments);
        };
    },
    
    after: function(times, func) {
        var count = 0;
        return function() {
            if (++count >= times) return func.apply(this, arguments);
        };
    },
    
    before: function(times, func) {
        var count = 0;
        return function() {
            if (count++ < times) return func.apply(this, arguments);
        };
    },
    
    once: function(func) {
        return _.before(2, func);
    },
    
    memoize: function(func, hasher) {
        var memoize = function(key) {
            var cache = memoize.cache;
            var address = '' + (hasher ? hasher.apply(this, arguments) : key);
            if (!_.has(cache, address)) cache[address] = func.apply(this, arguments);
            return cache[address];
        };
        memoize.cache = {};
        return memoize;
    },
    
    delay: function(func, wait) {
        var args = Array.prototype.slice.call(arguments, 2);
        return setTimeout(function() {
            return func.apply(func, args);
        }, wait);
    },
    
    defer: function(func) {
        return _.delay.apply(_, [func, 1].concat(Array.prototype.slice.call(arguments, 1)));
    },
    
    wrap: function(func, wrapper) {
        return _.partial(wrapper, func);
    },
    
    partial: function(func) {
        var boundArgs = Array.prototype.slice.call(arguments, 1);
        var bound = function() {
            var position = 0, length = boundArgs.length;
            var args = Array(length);
            for (var i = 0; i < length; i++) {
                args[i] = boundArgs[i] === _ ? arguments[position++] : boundArgs[i];
            }
            while (position < arguments.length) args.push(arguments[position++]);
            return func.apply(this, args);
        };
        return bound;
    },
    
    bind: function(func, context) {
        if (func.bind === Function.prototype.bind) {
            return Function.prototype.bind.apply(func, Array.prototype.slice.call(arguments, 1));
        }
        var args = Array.prototype.slice.call(arguments, 2);
        return function() {
            return func.apply(context, args.concat(Array.prototype.slice.call(arguments)));
        };
    },
    
    bindAll: function(obj) {
        var i, l, key;
        var funcs = Array.prototype.slice.call(arguments, 1);
        if (funcs.length === 0) funcs = _.functions(obj);
        for (i = 0, l = funcs.length; i < l; i++) {
            key = funcs[i];
            obj[key] = _.bind(obj[key], obj);
        }
        return obj;
    },
    
    functions: function(obj) {
        var names = [];
        for (var key in obj) {
            if (_.isFunction(obj[key])) names.push(key);
        }
        return names.sort();
    },
    
    methods: function(obj) {
        return _.functions(obj);
    },
    
    pluck: function(obj, key) {
        return _.map(obj, function(value) {
            return value == null ? undefined : value[key];
        });
    },
    
    where: function(obj, attrs) {
        return _.filter(obj, _.matches(attrs));
    },
    
    findWhere: function(obj, attrs) {
        return _.find(obj, _.matches(attrs));
    },
    
    max: function(obj, iteratee, context) {
        var result = -Infinity, computed;
        if (iteratee == null && obj != null) {
            for (var i = 0, l = obj.length; i < l; i++) {
                var value = obj[i];
                if (value > result) result = value;
            }
        } else {
            _.each(obj, function(value, index, list) {
                computed = iteratee ? iteratee.call(context, value, index, list) : value;
                if (computed > result || computed === -Infinity && result === -Infinity) {
                    result = computed;
                }
            });
        }
        return result;
    },
    
    min: function(obj, iteratee, context) {
        var result = Infinity, computed;
        if (iteratee == null && obj != null) {
            for (var i = 0, l = obj.length; i < l; i++) {
                var value = obj[i];
                if (value < result) result = value;
            }
        } else {
            _.each(obj, function(value, index, list) {
                computed = iteratee ? iteratee.call(context, value, index, list) : value;
                if (computed < result || computed === Infinity && result === Infinity) {
                    result = computed;
                }
            });
        }
        return result;
    },
    
    shuffle: function(obj) {
        return _.sample(obj, Infinity);
    },
    
    sampleSize: function(obj, n, guard) {
        if (n == null || guard) {
            if (obj && obj.length === +obj.length) return obj[_.random(obj.length - 1)];
            return undefined;
        }
        var sample = _.shuffle(obj);
        return sample.slice(0, Math.max(0, n));
    },
    
    sortByOrder: function(obj, iteratees, orders) {
        if (iteratees == null) return obj;
        if (!Array.isArray(iteratees)) iteratees = [iteratees];
        if (!Array.isArray(orders)) orders = [orders];
        iteratees = iteratees.map(function(iter, i) {
            if (Array.isArray(iter)) {
                return { iteratee: iter[0], sortOrder: orders[i] };
            }
            return { iteratee: iter, sortOrder: orders[i] };
        });
        return obj.map(function(item) {
            return iteratees.map(function(spec) {
                return spec.iteratee(item);
            });
        }).sortBy(function(specs) {
            return specs.map(function(spec, i) {
                return [spec, orders[i] !== 'desc'];
            });
        }).map(function(specs) {
            return obj[specs[0]];
        });
    },
    
    groupBy: function(obj, iteratee, context) {
        var result = {};
        iteratee = _.isFunction(iteratee) ? iteratee : function(x) { return x[iteratee]; };
        _.each(obj, function(value, key) {
            var groupKey = iteratee.call(context, value, key);
            (result[groupKey] || (result[groupKey] = [])).push(value);
        });
        return result;
    },
    
    countBy: function(obj, iteratee, context) {
        var result = {};
        iteratee = _.isFunction(iteratee) ? iteratee : function(x) { return x[iteratee]; };
        _.each(obj, function(value, key) {
            var keyVal = iteratee.call(context, value, key);
            result[keyVal] = (result[keyVal] || 0) + 1;
        });
        return result;
    },
    
    sortBy: function(obj, iteratee, context) {
        var iterateeFn = _.isFunction(iteratee) ? iteratee : function(x) { return x[iteratee]; };
        return _.pluck(_.map(_.chunk(obj, 1), function(value, index, list) {
            return {
                value: value[0],
                criteria: iterateeFn.call(context, value[0], index, list)
            };
        }).sortBy('criteria', 'asc'), 'value');
    },
    
    sortByDesc: function(obj, iteratee, context) {
        var iterateeFn = _.isFunction(iteratee) ? iteratee : function(x) { return x[iteratee]; };
        return _.pluck(_.map(_.chunk(obj, 1), function(value, index, list) {
            return {
                value: value[0],
                criteria: iterateeFn.call(context, value[0], index, list)
            };
        }).sortBy('criteria', 'desc'), 'value');
    },
    
    iteratee: function(value) {
        if (typeof value === 'function') return value;
        if (typeof value === 'string') return _.property(value);
        return _.identity;
    },
    
    random: function(min, max) {
        if (max == null) {
            max = min;
            min = 0;
        }
        return min + Math.floor(Math.random() * (max - min + 1));
    },
    
    now: Date.now || function() {
        return new Date().getTime();
    },
    
    throttle: function(func, wait, options) {
        var context, args, timeout, result;
        var previous = 0;
        if (!options) options = {};
        var later = function() {
            previous = options.leading === false ? 0 : _.now();
            timeout = null;
            result = func.apply(context, args);
            if (!timeout) context = args = null;
        };
        var throttled = function() {
            var now = _.now();
            if (!previous && options.leading === false) previous = now;
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
            if (remaining <= 0 || remaining > wait) {
                if (timeout) {
                    clearTimeout(timeout);
                    timeout = null;
                }
                previous = now;
                result = func.apply(context, args);
                if (!timeout) context = args = null;
            } else if (!timeout && options.trailing !== false) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
        throttled.cancel = function() {
            clearTimeout(timeout);
            previous = 0;
            timeout = context = args = null;
        };
        return throttled;
    },
    
    debounce: function(func, wait, immediate) {
        var timeout, result;
        var later = function() {
            timeout = null;
            if (!immediate) result = func.apply(context, args);
            if (!timeout) context = args = null;
        };
        var debounced = function() {
            context = this;
            args = arguments;
            var callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) result = func.apply(context, args);
            if (!timeout) context = args = null;
            return result;
        };
        debounced.cancel = function() {
            clearTimeout(timeout);
            timeout = context = args = null;
        };
        return debounced;
    },
    
    wrap: function(func, wrapper) {
        return _.partial(wrapper, func);
    },
    
    times: function(n, iteratee, context) {
        var accum = Array(Math.max(0, n));
        iteratee = _.bind(iteratee, context);
        for (var i = 0; i < n; i++) accum[i] = iteratee(i);
        return accum;
    },
    
    result: function(obj, path, fallback) {
        var value = obj;
        if (typeof path === 'string') path = path.split('.');
        for (var i = 0, l = path.length; i < l; i++) {
            if (value == null) return fallback;
            value = value[path[i]];
        }
        if (value === void 0) return fallback;
        return value;
    },
    
    unique: function(array, isSorted, iteratee, context) {
        if (!_.isBoolean(isSorted)) {
            context = iteratee;
            iteratee = isSorted;
            isSorted = false;
        }
        if (iteratee != null) {
            iteratee = _.iteratee(iteratee);
        }
        var result = [];
        var seen = [];
        for (var i = 0, l = array.length; i < l; i++) {
            var value = array[i];
            var computed = iteratee ? iteratee.call(context, value, i, array) : value;
            if (isSorted) {
                if (!i || seen !== computed) {
                    result.push(value);
                    seen = computed;
                }
            } else if (iteratee) {
                if (seen.indexOf(computed) < 0) {
                    seen.push(computed);
                    result.push(value);
                }
            } else if (result.indexOf(value) < 0) {
                result.push(value);
            }
        }
        return result;
    }
};

function parseHTML(html) {
    var elements = [];
    var tagStack = [];
    var textBuffer = '';
    var currentNode = null;
    
    function createNode(type, attrs, parent) {
        return {
            type: type,
            tagName: type,
            attributes: attrs || {},
            parent: parent || null,
            children: [],
            textContent: '',
            innerHTML: '',
            outerHTML: ''
        };
    }
    
    function processText() {
        if (textBuffer.trim()) {
            var textNode = {
                type: 'text',
                textContent: textBuffer,
                nodeValue: textBuffer
            };
            if (currentNode) {
                currentNode.children.push(textNode);
                currentNode.textContent += textBuffer;
            } else {
                elements.push(textNode);
            }
        }
        textBuffer = '';
    }
    
    var tagRegex = /<(\/?)([\w-]+)([^>]*)>/g;
    var attrRegex = /([\w-]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|(\S+)))?/g;
    var match;
    
    while ((match = tagRegex.exec(html)) !== null) {
        processText();
        
        var isClosing = match[1] === '/';
        var tagName = match[2].toLowerCase();
        var attrString = match[3];
        var attrs = {};
        
        var attrMatch;
        while ((attrMatch = attrRegex.exec(attrString)) !== null) {
            var attrName = attrMatch[1];
            var attrValue = attrMatch[2] || attrMatch[3] || attrMatch[4] || '';
            attrs[attrName] = attrValue;
        }
        
        if (isClosing) {
            if (tagStack.length > 0) {
                var closedNode = tagStack.pop();
                if (tagStack.length > 0) {
                    tagStack[tagStack.length - 1].children.push(closedNode);
                } else {
                    elements.push(closedNode);
                }
                currentNode = tagStack.length > 0 ? tagStack[tagStack.length - 1] : null;
            }
        } else {
            var voidTags = ['br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr'];
            var newNode = createNode(tagName, attrs, currentNode);
            
            if (currentNode) {
                currentNode.children.push(newNode);
            } else {
                elements.push(newNode);
            }
            
            if (voidTags.indexOf(tagName) === -1) {
                tagStack.push(newNode);
                currentNode = newNode;
            }
        }
    }
    
    processText();
    
    return {
        root: elements.length === 1 ? elements[0] : elements,
        elements: elements
    };
}

function querySelectorAll(node, selector) {
    if (!node) return [];
    
    var results = [];
    var simpleClasses = selector.match(/\.([\w-]+)/g);
    var simpleTags = selector.match(/^([\w-]+)/);
    var simpleId = selector.match(/#([\w-]+)/);
    
    function walk(n) {
        if (!n) return;
        
        var match = true;
        
        if (simpleId && n.attributes && n.attributes.id !== simpleId[1]) {
            match = false;
        }
        
        if (match && simpleTags && n.tagName !== simpleTags[1].toLowerCase()) {
            if (simpleClasses) {
                match = false;
            } else {
                return;
            }
        }
        
        if (match && simpleClasses) {
            for (var i = 0; i < simpleClasses.length; i++) {
                var cls = simpleClasses[i].substring(1);
                if (!n.attributes || !n.attributes.class || n.attributes.class.indexOf(cls) === -1) {
                    match = false;
                    break;
                }
            }
        }
        
        if (match) {
            results.push(n);
        }
        
        if (n.children) {
            for (var i = 0; i < n.children.length; i++) {
                walk(n.children[i]);
            }
        }
    }
    
    walk(node);
    
    return results;
}

function querySelector(node, selector) {
    var results = querySelectorAll(node, selector);
    return results.length > 0 ? results[0] : null;
}

function getAttribute(node, attrName) {
    if (!node || !node.attributes) return undefined;
    return node.attributes[attrName];
}

function getText(node) {
    if (!node) return '';
    if (node.type === 'text') return node.textContent || '';
    
    var text = '';
    if (node.children) {
        for (var i = 0; i < node.children.length; i++) {
            text += getText(node.children[i]);
        }
    }
    return text;
}

function getHTML(node) {
    if (!node) return '';
    
    var html = '<' + node.tagName;
    
    if (node.attributes) {
        for (var attr in node.attributes) {
            if (node.attributes.hasOwnProperty(attr)) {
                html += ' ' + attr + '="' + (node.attributes[attr] || '') + '"';
            }
        }
    }
    
    if (node.children && node.children.length > 0) {
        html += '>';
        for (var i = 0; i < node.children.length; i++) {
            html += getHTML(node.children[i]);
        }
        html += '</' + node.tagName + '>';
    } else {
        var voidTags = ['br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'param', 'source', 'track', 'wbr'];
        if (voidTags.indexOf(node.tagName) !== -1) {
            html += ' />';
        } else {
            html += '></' + node.tagName + '>';
        }
    }
    
    return html;
}

function $(selector) {
    if (typeof selector === 'string') {
        return querySelector(this.root || this.elements ? this.elements[0] : null, selector);
    }
    return selector;
}

$.find = function(selector) {
    return querySelectorAll(this, selector);
};

$.children = function(selector) {
    if (!this.children) return [];
    if (!selector) return this.children;
    return this.children.filter(function(child) {
        return child.tagName === selector;
    });
};

$.parent = function() {
    return this.parent;
};

$.attr = function(name) {
    if (typeof name === 'string') {
        return this.attributes ? this.attributes[name] : undefined;
    }
    var attrs = {};
    for (var key in name) {
        if (this.attributes && this.attributes.hasOwnProperty(key)) {
            attrs[key] = this.attributes[key];
        }
    }
    return attrs;
};

$.text = function() {
    return getText(this);
};

$.html = function() {
    return getHTML(this);
};

$.text = function(val) {
    if (val !== undefined) {
        this.textContent = val;
        return this;
    }
    return getText(this);
};

$.html = function(val) {
    if (val !== undefined) {
        this.children = [];
        var parsed = parseHTML(val);
        this.children = parsed.elements;
        return this;
    }
    return getHTML(this);
};

$.find = function(selector) {
    var results = querySelectorAll(this, selector);
    var wrapper = function(node) {
        return Object.assign({}, $, {
            root: this.root,
            elements: this.elements,
            [0]: node
        });
    }.bind(this);
    
    results.find = function(sel) {
        for (var i = 0; i < this.length; i++) {
            var found = querySelectorAll(this[i], sel);
            if (found.length > 0) return wrapper(found[0]);
        }
        return null;
    };
    
    results.each = function(callback) {
        for (var i = 0; i < this.length; i++) {
            callback.call(wrapper(this[i]), i, this[i]);
        }
        return this;
    };
    
    return results;
};

$.each = function(callback) {
    if (this.children) {
        for (var i = 0; i < this.children.length; i++) {
            callback.call($.bind(this.children[i]), i, this.children[i]);
        }
    }
    return this;
};

$.map = function(callback) {
    var results = [];
    if (this.children) {
        for (var i = 0; i < this.children.length; i++) {
            var result = callback.call(this.children[i], i, this.children[i]);
            if (result !== null && result !== undefined) {
                results.push(result);
            }
        }
    }
    return results;
};

function load(html) {
    var parsed = parseHTML(html);
    
    var result = Object.assign({}, $, {
        root: parsed.elements.length === 1 ? parsed.elements[0] : parsed.elements,
        elements: parsed.elements,
        length: parsed.elements.length,
        [0]: parsed.elements[0]
    });
    
    result.find = function(selector) {
        var node = this[0] || this.elements[0];
        var results = querySelectorAll(node, selector);
        results.find = function(sel) {
            for (var i = 0; i < this.length; i++) {
                var found = querySelectorAll(this[i], sel);
                if (found.length > 0) return wrapper(found[0]);
            }
            return null;
        };
        return results;
    };
    
    result.each = function(callback) {
        var elements = this.children || this.elements || [];
        for (var i = 0; i < elements.length; i++) {
            var wrapped = Object.assign({}, $, {
                root: this.root,
                elements: this.elements,
                [0]: elements[i]
            });
            callback.call(wrapped, i, elements[i]);
        }
        return this;
    };
    
    return result;
}

function log() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.log.apply(console, args);
    }
}

function print() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.log.apply(console, args);
    }
}

function println() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.log.apply(console, args);
    }
}

function printLog() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.log.apply(console, args);
    }
}

function printDebug() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.debug.apply(console, args);
    }
}

function printError() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.error.apply(console, args);
    }
}

function printInfo() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.info.apply(console, args);
    }
}

function printWarn() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined') {
        console.warn.apply(console, args);
    }
}

function clear() {
    if (typeof console !== 'undefined' && console.clear) {
        console.clear();
    }
}

function count() {
    var label = arguments[0] || 'default';
    if (typeof console !== 'undefined' && console.count) {
        console.count(label);
    }
}

function assert() {
    var assertion = arguments[0];
    var args = Array.prototype.slice.call(arguments, 1);
    if (typeof console !== 'undefined' && console.assert) {
        console.assert(assertion, args.join(' '));
    }
}

function printTable() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined' && console.table) {
        console.table.apply(console, args);
    }
}

function printTime() {
    var label = arguments[0] || 'default';
    if (typeof console !== 'undefined' && console.time) {
        console.time(label);
    }
}

function printTimeEnd() {
    var label = arguments[0] || 'default';
    if (typeof console !== 'undefined' && console.timeEnd) {
        console.timeEnd(label);
    }
}

function printTrace() {
    if (typeof console !== 'undefined' && console.trace) {
        console.trace();
    }
}

function printGroup() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined' && console.group) {
        console.group.apply(console, args);
    }
}

function printGroupEnd() {
    if (typeof console !== 'undefined' && console.groupEnd) {
        console.groupEnd();
    }
}

function printGroupCollapsed() {
    var args = Array.prototype.slice.call(arguments);
    if (typeof console !== 'undefined' && console.groupCollapsed) {
        console.groupCollapsed.apply(console, args);
    }
}

function require() {
    var module = arguments[0];
    if (module === 'crypto' || module === 'Crypto') {
        return Crypto;
    }
    return null;
}

function delay(ms) {
    return new Promise(function(resolve) {
        setTimeout(resolve, ms);
    });
}

function sleep(ms) {
    return delay(ms);
}

function timeout(ms) {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            reject(new Error('Timeout'));
        }, ms);
    });
}

function http_build_query(formdata, numeric_prefix, arg_separator) {
    var components = [];
    var separator = arg_separator || '&';
    
    function buildQuery(data, prefix) {
        var parts = [];
        
        if (typeof data === 'object') {
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var newKey = prefix ? prefix + '[' + key + ']' : key;
                    parts = parts.concat(buildQuery(data[key], newKey));
                }
            }
        } else {
            parts.push(encodeURIComponent(prefix) + '=' + encodeURIComponent(data));
        }
        
        return parts;
    }
    
    components = buildQuery(formdata, numeric_prefix);
    return components.join(separator);
}

function parse_str(str, result) {
    var pairs = str.replace(/^\?/, '').split('&');
    result = result || {};
    
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i].split('=');
        var key = decodeURIComponent(pair[0]);
        var value = pair.length > 1 ? decodeURIComponent(pair[1].replace(/\+/g, ' ')) : '';
        
        if (key.match(/\[/)) {
            var keys = key.match(/[^\[\]]+/g);
            var target = result;
            for (var j = 0; j < keys.length - 1; j++) {
                if (!target[keys[j]]) target[keys[j]] = {};
                target = target[keys[j]];
            }
            target[keys[keys.length - 1]] = value;
        } else {
            result[key] = value;
        }
    }
    
    return result;
}

function parse_url(str, component) {
    var pattern = /^(?:([A-Za-z]+):)?(\/{0,3})([0-9.\-A-Za-z]+)(?::(\d+))?(?:\/([^?#]*))?(?:\?([^#]*))?(?:#(.*))?$/;
    var matches = str.match(pattern);
    
    if (!matches) return false;
    
    var result = {
        scheme: matches[1],
        fragment: matches[7],
        query: matches[6],
        path: matches[5],
        port: matches[4],
        host: matches[3],
        password: '',
        user: ''
    };
    
    var userPass = matches[3].match(/^([^\@]+)\@(.*)$/);
    if (userPass) {
        var userPassSplit = userPass[1].split(':');
        result.user = userPassSplit[0];
        result.password = userPassSplit[1] || '';
        result.host = userPass[2];
    }
    
    if (component !== undefined) {
        return result[component];
    }
    
    return result;
}

function json_encode(obj) {
    return JSON.stringify(obj);
}

function json_decode(str) {
    return JSON.parse(str);
}

function url_encode(str) {
    return encodeURIComponent(str);
}

function url_decode(str) {
    return decodeURIComponent(str);
}

function html_encode(str) {
    return str.replace(/&/g, '&amp;')
               .replace(/</g, '&lt;')
               .replace(/>/g, '&gt;')
               .replace(/"/g, '&quot;')
               .replace(/'/g, '&#x27;')
               .replace(/\//g, '&#x2F;');
}

function html_decode(str) {
    return str.replace(/&amp;/g, '&')
               .replace(/&lt;/g, '<')
               .replace(/&gt;/g, '>')
               .replace(/&quot;/g, '"')
               .replace(/&#x27;/g, "'")
               .replace(/&#x2F;/g, '/');
}

function trim(str) {
    return str.trim();
}

function ltrim(str) {
    return str.replace(/^\s+/, '');
}

function rtrim(str) {
    return str.replace(/\s+$/, '');
}

function strtolower(str) {
    return str.toLowerCase();
}

function strtoupper(str) {
    return str.toUpperCase();
}

function substr(str, start, length) {
    if (length === undefined) {
        return str.substring(start);
    }
    return str.substring(start, start + length);
}

function strlen(str) {
    return str.length;
}

function strpos(haystack, needle, offset) {
    var index = haystack.indexOf(needle, offset);
    return index === -1 ? false : index;
}

function strrpos(haystack, needle, offset) {
    var index = haystack.lastIndexOf(needle, offset);
    return index === -1 ? false : index;
}

function str_replace(search, replace, subject) {
    if (Array.isArray(subject)) {
        return subject.map(function(item) {
            return str_replace(search, replace, item);
        });
    }
    return subject.split(search).join(replace);
}

function str_repeat(str, times) {
    return str.repeat(times);
}

function str_split(str, length) {
    if (length === undefined) length = 1;
    var result = [];
    for (var i = 0; i < str.length; i += length) {
        result.push(str.substring(i, i + length));
    }
    return result;
}

function explode(delimiter, string) {
    return string.split(delimiter);
}

function implode(glue, pieces) {
    if (Array.isArray(pieces)) {
        return pieces.join(glue);
    }
    return pieces;
}

function join(glue, pieces) {
    return implode(glue, pieces);
}

function md5(str) {
    return Crypto.MD5(str);
}

function sha1(str) {
    return Crypto.sha1(str);
}

function sha256(str) {
    return Crypto.sha1(str);
}

function base64_encode(str) {
    return Crypto.base64encode(str);
}

function base64_decode(str) {
    return Crypto.base64decode(str);
}

function urlencode(str) {
    return encodeURIComponent(str);
}

function urldecode(str) {
    return decodeURIComponent(str);
}

function rawurlencode(str) {
    return encodeURIComponent(str).replace(/!/g, '%21').replace(/'/g, '%27').replace(/\(/g, '%28').replace(/\)/g, '%29').replace(/\*/g, '%2A');
}

function rawurldecode(str) {
    return decodeURIComponent(str.replace(/\+/g, ' '));
}

function number_format(number, decimals, decPoint, thousandsSep) {
    number = (number + '').replace(/[^0-9+\-Ee.]/g, '');
    var n = !isFinite(+number) ? 0 : +number;
    var prec = !isFinite(+decimals) ? 0 : Math.abs(decimals);
    var sep = (typeof thousandsSep === 'undefined') ? ',' : thousandsSep;
    var dec = (typeof decPoint === 'undefined') ? '.' : decPoint;
    var s = '';
    var toFixedFix = function(n, prec) {
        return '' + (Math.round(n * Math.pow(10, prec)) / Math.pow(10, prec));
    };
    s = (prec ? toFixedFix(n, prec) : toFixedFix(Math.round(n), prec)).split('.');
    if (s[0].length > 3) {
        s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
    }
    if ((s[1] || '').length < prec) {
        s[1] = s[1] || '';
        s[1] += new Array(prec - s[1].length + 1).join('0');
    }
    return s.join(dec);
}

function sprintf() {
    var args = Array.prototype.slice.call(arguments);
    var format = args.shift();
    var i = 0;
    return format.replace(/%s/g, function() {
        return i < args.length ? args[i++] : '';
    });
}

function printf() {
    var args = Array.prototype.slice.call(arguments);
    var format = args.shift();
    var result = sprintf.apply(null, [format].concat(args));
    if (typeof console !== 'undefined') {
        console.log(result);
    }
    return result;
}

function in_array(needle, haystack, strict) {
    for (var i = 0; i < haystack.length; i++) {
        if (haystack[i] === needle || (!strict && haystack[i] == needle)) {
            return true;
        }
    }
    return false;
}

function array_keys(arr) {
    return _.keys(arr);
}

function array_values(arr) {
    return _.values(arr);
}

function array_merge() {
    var result = [];
    for (var i = 0; i < arguments.length; i++) {
        if (Array.isArray(arguments[i])) {
            result = result.concat(arguments[i]);
        }
    }
    return result;
}

function array_push(arr, val) {
    return arr.push(val);
}

function array_pop(arr) {
    return arr.pop();
}

function array_shift(arr) {
    return arr.shift();
}

function array_unshift(arr, val) {
    return arr.unshift(val);
}

function array_slice(arr, offset, length) {
    return arr.slice(offset, length);
}

function array_splice(arr, offset, length, replace) {
    return arr.splice(offset, length, replace);
}

function array_reverse(arr) {
    return arr.reverse();
}

function array_sort(arr) {
    return arr.sort();
}

function array_unique(arr) {
    return _.uniq(arr);
}

function array_search(needle, haystack, strict) {
    for (var i = 0; i < haystack.length; i++) {
        if (haystack[i] === needle || (!strict && haystack[i] == needle)) {
            return i;
        }
    }
    return false;
}

function array_key_exists(key, arr) {
    return arr.hasOwnProperty(key);
}

function count(arr) {
    if (Array.isArray(arr)) return arr.length;
    return Object.keys(arr).length;
}

function sizeof(arr) {
    return count(arr);
}

function range(start, end, step) {
    if (step === undefined) step = 1;
    var result = [];
    if (typeof start !== 'number' || typeof end !== 'number') {
        for (var i = start.charCodeAt(0); i <= end.charCodeAt(0); i += step) {
            result.push(String.fromCharCode(i));
        }
    } else {
        for (var i = start; i <= end; i += step) {
            result.push(i);
        }
    }
    return result;
}

function array_chunk(arr, size) {
    return _.chunk(arr, size);
}

function array_filter(arr, callback) {
    return _.filter(arr, callback);
}

function array_map(callback) {
    var arr = arguments[0];
    var args = Array.prototype.slice.call(arguments, 1);
    return arr.map(function(item) {
        return callback.apply(null, [item].concat(args));
    });
}

function sort(arr, flags) {
    arr.sort(function(a, b) {
        if (a < b) return -1;
        if (a > b) return 1;
        return 0;
    });
}

function rsort(arr, flags) {
    arr.sort(function(a, b) {
        if (a > b) return -1;
        if (a < b) return 1;
        return 0;
    });
}

function ksort(arr, flags) {
    Object.keys(arr).sort().forEach(function(key) {
        var value = arr[key];
        delete arr[key];
        arr[key] = value;
    });
}

function shuffle(arr) {
    arr = _.shuffle(arr);
}

function boolval(mixed_var) {
    return Boolean(mixed_var);
}

function intval(mixed_var, base) {
    if (base === undefined) base = 10;
    return parseInt(mixed_var, base);
}

function floatval(mixed_var) {
    return parseFloat(mixed_var);
}

function strval(mixed_var) {
    return String(mixed_var);
}

function empty(mixed_var) {
    if (mixed_var === null || mixed_var === undefined) return true;
    if (typeof mixed_var === 'string' && mixed_var === '') return true;
    if (Array.isArray(mixed_var) && mixed_var.length === 0) return true;
    if (typeof mixed_var === 'object' && Object.keys(mixed_var).length === 0) return true;
    return false;
}

function isset() {
    for (var i = 0; i < arguments.length; i++) {
        if (arguments[i] === undefined) return false;
    }
    return true;
}

function is_array(mixed_var) {
    return Array.isArray(mixed_var);
}

function is_bool(mixed_var) {
    return typeof mixed_var === 'boolean';
}

function is_float(mixed_var) {
    return typeof mixed_var === 'number' && mixed_var % 1 !== 0;
}

function is_int(mixed_var) {
    return typeof mixed_var === 'number' && mixed_var % 1 === 0;
}

function is_integer(mixed_var) {
    return is_int(mixed_var);
}

function is_null(mixed_var) {
    return mixed_var === null;
}

function is_numeric(mixed_var) {
    return typeof mixed_var === 'number' || typeof mixed_var === 'string' && !isNaN(mixed_var) && !isNaN(parseFloat(mixed_var));
}

function is_object(mixed_var) {
    return typeof mixed_var === 'object' && mixed_var !== null && !Array.isArray(mixed_var);
}

function is_string(mixed_var) {
    return typeof mixed_var === 'string';
}

function is_callable(mixed_var) {
    return typeof mixed_var === 'function';
}

function date(format, timestamp) {
    if (timestamp === undefined) timestamp = Date.now();
    var d = new Date(timestamp);
    var Y = d.getFullYear();
    var m = String(d.getMonth() + 1).padStart(2, '0');
    var d = String(d.getDate()).padStart(2, '0');
    var H = String(d.getHours()).padStart(2, '0');
    var i = String(d.getMinutes()).padStart(2, '0');
    var s = String(d.getSeconds()).padStart(2, '0');
    var j = d.getDay();
    var day_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    var month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    var result = format;
    result = result.replace(/Y/g, Y);
    result = result.replace(/m/g, m);
    result = result.replace(/d/g, d);
    result = result.replace(/H/g, H);
    result = result.replace(/i/g, i);
    result = result.replace(/s/g, s);
    result = result.replace(/j/g, j);
    result = result.replace(/D/g, day_names[j]);
    result = result.replace(/M/g, month_names[d.getMonth()]);
    
    return result;
}

function time() {
    return Math.floor(Date.now() / 1000);
}

function microtime(get_as_float) {
    var now = Date.now();
    if (get_as_float) return now / 1000;
    var seconds = Math.floor(now / 1000);
    var microseconds = String(now % 1000).padStart(3, '0');
    return microseconds + ' ' + seconds;
}

function strtotime(time, now) {
    if (now === undefined) now = Date.now();
    var d = new Date(now);
    
    var patterns = {
        'second': 1000,
        'minute': 60000,
        'hour': 3600000,
        'day': 86400000,
        'week': 604800000,
        'month': 2592000000,
        'year': 31536000000
    };
    
    var match = time.match(/(\d+)\s*(second|minute|hour|day|week|month|year)s?/i);
    if (match) {
        return now + parseInt(match[1]) * patterns[match[2].toLowerCase()];
    }
    
    var relativeMatch = time.match(/\+(\d+)\s*(second|minute|hour|day|week|month|year)s?/i);
    if (relativeMatch) {
        return now + parseInt(relativeMatch[1]) * patterns[relativeMatch[2].toLowerCase()];
    }
    
    var minusMatch = time.match(/-(\d+)\s*(second|minute|hour|day|week|month|year)s?/i);
    if (minusMatch) {
        return now - parseInt(minusMatch[1]) * patterns[minusMatch[2].toLowerCase()];
    }
    
    if (time === 'now') return now;
    
    return new Date(time).getTime();
}

function mktime() {
    var args = Array.prototype.slice.call(arguments);
    var d = new Date();
    if (args.length >= 1) d.setHours(args[0] || 0);
    if (args.length >= 2) d.setMinutes(args[1] || 0);
    if (args.length >= 3) d.setDate(args[2] || 1);
    if (args.length >= 4) d.setMonth((args[3] || 1) - 1);
    if (args.length >= 5) d.setFullYear(args[4] || 1970);
    if (args.length >= 6) d.setSeconds(args[5] || 0);
    return Math.floor(d.getTime() / 1000);
}

function getdate(timestamp) {
    if (timestamp === undefined) timestamp = Date.now();
    var d = new Date(timestamp);
    return {
        seconds: d.getSeconds(),
        minutes: d.getMinutes(),
        hours: d.getHours(),
        mday: d.getDate(),
        wday: d.getDay(),
        mon: d.getMonth() + 1,
        year: d.getFullYear(),
        yday: Math.floor((d - new Date(d.getFullYear(), 0, 1)) / 86400000),
        weekday: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][d.getDay()],
        month: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][d.getMonth()]
    };
}

function str_pad(input, pad_length, pad_string, pad_type) {
    var pad = '';
    var len = pad_length - input.length;
    if (len > 0) {
        if (pad_type === 'STR_PAD_LEFT') {
            for (var i = 0; i < len; i++) {
                pad += pad_string;
            }
            return pad + input;
        } else if (pad_type === 'STR_PAD_BOTH') {
            var left = Math.ceil(len / 2);
            var right = Math.floor(len / 2);
            for (var i = 0; i < left; i++) {
                pad += pad_string;
            }
            for (var i = 0; i < right; i++) {
                pad += pad_string;
            }
            return pad + input;
        } else {
            for (var i = 0; i < len; i++) {
                pad += pad_string;
            }
            return input + pad;
        }
    }
    return input;
}

function nl2br(str, is_xhtml) {
    var br = is_xhtml ? '<br />' : '<br>';
    return str.replace(/(?:\r\n|\r|\n)/g, br);
}

function strip_tags(str, allow) {
    if (allow) {
        var tags = '<' + allow.replace(/[^a-z0-9,]+/gi, '> <') + '>';
        var allowed = new RegExp(tags, 'gi');
        var tagsToRemove = /<\/?([a-z][a-z0-9]*)\b[^>]*>/gi;
        return str.replace(tagsToRemove, function($0, $1) {
            return allowed.test('<' + $1 + '>') ? $0 : '';
        });
    }
    return str.replace(/<[^>]*>/g, '');
}

function stripslashes(str) {
    return str.replace(/\\'/g, "'").replace(/\\"/g, '"').replace(/\\\\/g, '\\');
}

function addslashes(str) {
    return str.replace(/[\\"']/g, '\\$&').replace(/\u0000/g, '\\0');
}

function htmlspecialchars(str, quote_style, charset, double_encode) {
    var symbol_arr = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;'
    };
    if (!noquotes) symbol_arr['"'] = '&quot;';
    if (!noquotes) symbol_arr["'"] = '&#039;';
    var _symbol = symbol_arr;
    
    var pattern = /[&<>"']/g;
    return str.replace(pattern, function(s) {
        return _symbol[s];
    });
}

function wordwrap(str, width, break_char, cut) {
    width = width || 75;
    break_char = break_char || '\n';
    cut = cut || false;
    
    if (width <= 0) return str;
    
    var lines = str.split('\n');
    for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        if (line.length <= width) continue;
        
        var words = line.split(' ');
        var newLine = '';
        var currentLength = 0;
        
        for (var j = 0; j < words.length; j++) {
            var word = words[j];
            var wordLength = word.length;
            
            if (currentLength + wordLength + 1 > width) {
                if (cut && wordLength > width) {
                    while (word.length > 0) {
                        newLine += word.substring(0, width - currentLength) + break_char;
                        word = word.substring(width - currentLength);
                        currentLength = 0;
                    }
                } else {
                    newLine += break_char;
                    currentLength = 0;
                }
            }
            
            if (currentLength > 0) {
                newLine += ' ';
                currentLength++;
            }
            newLine += word;
            currentLength += wordLength;
        }
        
        lines[i] = newLine;
    }
    
    return lines.join('\n');
}

function ucfirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function lcfirst(str) {
    return str.charAt(0).toLowerCase() + str.slice(1);
}

function ucwords(str) {
    return str.replace(/(?:^|\s)\S/g, function(c) { return c.toUpperCase(); });
}

function strrev(str) {
    return str.split('').reverse().join('');
}

function crc32(str) {
    var table = [];
    for (var n = 0; n < 256; n++) {
        var c = n;
        for (var k = 0; k < 8; k++) {
            c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
        }
        table[n] = c;
    }
    
    var crc = 0xffffffff;
    for (var i = 0; i < str.length; i++) {
        crc = table[(crc ^ str.charCodeAt(i)) & 0xff] ^ (crc >>> 8);
    }
    return (crc ^ 0xffffffff) >>> 0;
}

function hex2bin(hex) {
    var bytes = [];
    for (var i = 0; i < hex.length; i += 2) {
        bytes.push(String.fromCharCode(parseInt(hex.substr(i, 2), 16)));
    }
    return bytes.join('');
}

function bin2hex(str) {
    var hex = '';
    for (var i = 0; i < str.length; i++) {
        hex += str.charCodeAt(i).toString(16).padStart(2, '0');
    }
    return hex;
}

function str_rot13(str) {
    return str.replace(/[a-zA-Z]/g, function(c) {
        var start = c <= 'Z' ? 65 : 97;
        return String.fromCharCode(start + (c.charCodeAt(0) - start + 13) % 26);
    });
}

function levenshtein(str1, str2, cost_ins, cost_rep, cost_del) {
    cost_ins = cost_ins || 1;
    cost_rep = cost_rep || 1;
    cost_del = cost_del || 1;
    
    var m = str1.length;
    var n = str2.length;
    
    var d = [];
    for (var i = 0; i <= m; i++) {
        d[i] = [i];
    }
    for (var j = 0; j <= n; j++) {
        d[0][j] = j;
    }
    
    for (var j = 1; j <= n; j++) {
        for (var i = 1; i <= m; i++) {
            if (str1[i - 1] === str2[j - 1]) {
                d[i][j] = d[i - 1][j - 1];
            } else {
                d[i][j] = Math.min(
                    d[i - 1][j] + cost_ins,
                    d[i][j - 1] + cost_del,
                    d[i - 1][j - 1] + cost_rep
                );
            }
        }
    }
    
    return d[m][n];
}

function soundex(str) {
    str = str.toUpperCase();
    var s = str.charAt(0);
    var a = str.split('');
    var codes = {
        A: '', E: '', I: '', O: '', U: '', H: '', W: '', Y: '',
        B: '1', F: '1', P: '1', V: '1',
        C: '2', G: '2', J: '2', K: '2', Q: '2', S: '2', X: '2', Z: '2',
        D: '3', T: '3',
        L: '4',
        M: '5', N: '5',
        R: '6'
    };
    
    var prev = '';
    for (var i = 1; i < a.length; i++) {
        var code = codes[a[i]];
        if (code && code !== prev) {
            s += code;
            if (s.length === 4) break;
            if (code !== '0') prev = code;
        }
    }
    
    return (s + '000').substring(0, 4);
}

function metaphone(str, max_phonemes) {
    str = str.toUpperCase();
    max_phonemes = max_phonemes || 0;
    
    var result = '';
    var i = 0;
    var length = str.length;
    
    var vowels = 'AEIOU';
    var soft = ['X', 'S', 'J', 'Y', 'K', 'G', 'P', 'B', 'V', 'F', 'Z'];
    var letters = str.split('');
    
    if (letters[0] === 'A') result += 'A';
    if (letters[0] === 'E') result += 'E';
    if (letters[0] === 'I') result += 'I';
    if (letters[0] === 'O') result += 'O';
    if (letters[0] === 'U') result += 'U';
    
    for (var pos = 0; pos < length && (max_phonemes === 0 || result.length < max_phonemes); pos++) {
        var letter = letters[pos];
        
        if (vowels.indexOf(letter) !== -1) {
            continue;
        }
        
        switch (letter) {
            case 'B':
                if (letters[pos + 1] !== 'H') result += 'P';
                break;
            case 'C':
                if (letters[pos + 1] === 'I' && vowels.indexOf(letters[pos + 2]) !== -1) {
                    result += 'S';
                } else if (letters[pos + 1] === 'H') {
                    result += 'X';
                } else {
                    result += 'K';
                }
                break;
            case 'D':
                if (letters[pos + 1] === 'G' && vowels.indexOf(letters[pos + 2]) !== -1) {
                    result += 'J';
                } else {
                    result += 'T';
                }
                break;
            case 'G':
                if (letters[pos + 1] === 'H') {
                    if (vowels.indexOf(letters[pos + 2]) === -1) {
                        pos++;
                    } else {
                        result += 'F';
                    }
                } else if (letters[pos + 1] === 'N') {
                    result += 'K';
                } else if (soft.indexOf(letter) !== -1) {
                    result += 'K';
                } else {
                    result += 'K';
                }
                break;
            case 'H':
                if (vowels.indexOf(letters[pos + 1]) !== -1 || (pos === 0 || vowels.indexOf(letters[pos - 1]) !== -1)) {
                    result += 'H';
                }
                break;
            case 'K':
                if (letters[pos - 1] !== 'C') result += 'K';
                break;
            case 'P':
                if (letters[pos + 1] === 'H') {
                    result += 'F';
                } else {
                    result += 'P';
                }
                break;
            case 'Q':
                result += 'K';
                break;
            case 'S':
                if (letters[pos + 1] === 'H') {
                    result += 'X';
                } else if (letters[pos + 1] === 'I' && (letters[pos + 2] === 'O' || letters[pos + 2] === 'A')) {
                    result += 'X';
                } else {
                    result += 'S';
                }
                break;
            case 'T':
                if (letters[pos + 1] === 'I' && (letters[pos + 2] === 'O' || letters[pos + 2] === 'A')) {
                    result += 'X';
                } else if (letters[pos + 1] === 'H') {
                    result += '0';
                } else {
                    result += 'T';
                }
                break;
            case 'V':
                result += 'F';
                break;
            case 'W':
                if (vowels.indexOf(letters[pos + 1]) !== -1) {
                    result += 'W';
                }
                break;
            case 'X':
                result += 'KS';
                break;
            case 'Y':
                if (vowels.indexOf(letters[pos + 1]) !== -1) {
                    result += 'Y';
                }
                break;
            case 'Z':
                result += 'S';
                break;
            default:
                result += letter;
        }
        
        if (max_phonemes > 0 && result.length >= max_phonemes) break;
    }
    
    return result;
}

function deg2rad(degrees) {
    return degrees * (Math.PI / 180);
}

function rad2deg(radians) {
    return radians * (180 / Math.PI);
}

function max(values) {
    if (Array.isArray(values)) {
        values = values.filter(function(v) { return !isNaN(v); });
        return values.length > 0 ? Math.max.apply(null, values) : 0;
    }
    return Math.max.apply(null, arguments);
}

function min(values) {
    if (Array.isArray(values)) {
        values = values.filter(function(v) { return !isNaN(v); });
        return values.length > 0 ? Math.min.apply(null, values) : 0;
    }
    return Math.min.apply(null, arguments);
}

function abs(value) {
    return Math.abs(value);
}

function ceil(value) {
    return Math.ceil(value);
}

function floor(value) {
    return Math.floor(value);
}

function round(value, precision) {
    var multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
}

function sqrt(value) {
    return Math.sqrt(value);
}

function pow(base, exponent) {
    return Math.pow(base, exponent);
}

function exp(value) {
    return Math.exp(value);
}

function log(value, base) {
    if (base === undefined) return Math.log(value);
    return Math.log(value) / Math.log(base);
}

function sin(value) {
    return Math.sin(value);
}

function cos(value) {
    return Math.cos(value);
}

function tan(value) {
    return Math.tan(value);
}

function asin(value) {
    return Math.asin(value);
}

function acos(value) {
    return Math.acos(value);
}

function atan(value) {
    return Math.atan(value);
}

function atan2(y, x) {
    return Math.atan2(y, x);
}

function hypot() {
    var sum = 0;
    for (var i = 0; i < arguments.length; i++) {
        sum += arguments[i] * arguments[i];
    }
    return Math.sqrt(sum);
}

function pi() {
    return Math.PI;
}

function rand(min, max) {
    min = min || 0;
    max = max || 2147483647;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function mt_rand(min, max) {
    return rand(min, max);
}

function getrandmax() {
    return 2147483647;
}

function mt_getrandmax() {
    return 2147483647;
}

function array_rand(arr, num) {
    if (num === undefined) {
        var index = Math.floor(Math.random() * arr.length);
        return arr[index];
    }
    
    var keys = [];
    var copy = arr.slice();
    for (var i = 0; i < num && copy.length > 0; i++) {
        var index = Math.floor(Math.random() * copy.length);
        keys.push(copy[index]);
        copy.splice(index, 1);
    }
    return keys;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        Crypto: Crypto,
        _: _,
        load: load,
        $: $,
        log: log,
        print: print,
        println: println,
        printLog: printLog,
        printDebug: printDebug,
        printError: printError,
        printInfo: printInfo,
        printWarn: printWarn,
        clear: clear,
        count: count,
        assert: assert,
        printTable: printTable,
        printTime: printTime,
        printTimeEnd: printTimeEnd,
        printTrace: printTrace,
        printGroup: printGroup,
        printGroupEnd: printGroupEnd,
        printGroupCollapsed: printGroupCollapsed,
        require: require,
        delay: delay,
        sleep: sleep,
        timeout: timeout,
        http_build_query: http_build_query,
        parse_str: parse_str,
        parse_url: parse_url,
        json_encode: json_encode,
        json_decode: json_decode,
        url_encode: url_encode,
        url_decode: url_decode,
        html_encode: html_encode,
        html_decode: html_decode,
        trim: trim,
        ltrim: ltrim,
        rtrim: rtrim,
        strtolower: strtolower,
        strtoupper: strtoupper,
        substr: substr,
        strlen: strlen,
        strpos: strpos,
        strrpos: strrpos,
        str_replace: str_replace,
        str_repeat: str_repeat,
        str_split: str_split,
        explode: explode,
        implode: implode,
        join: join,
        md5: md5,
        sha1: sha1,
        sha256: sha256,
        base64_encode: base64_encode,
        base64_decode: base64_decode,
        urlencode: urlencode,
        urldecode: urldecode,
        rawurlencode: rawurlencode,
        rawurldecode: rawurldecode,
        number_format: number_format,
        sprintf: sprintf,
        printf: printf,
        in_array: in_array,
        array_keys: array_keys,
        array_values: array_values,
        array_merge: array_merge,
        array_push: array_push,
        array_pop: array_pop,
        array_shift: array_shift,
        array_unshift: array_unshift,
        array_slice: array_slice,
        array_splice: array_splice,
        array_reverse: array_reverse,
        array_sort: array_sort,
        array_unique: array_unique,
        array_search: array_search,
        array_key_exists: array_key_exists,
        count: count,
        sizeof: sizeof,
        range: range,
        array_chunk: array_chunk,
        array_filter: array_filter,
        array_map: array_map,
        sort: sort,
        rsort: rsort,
        ksort: ksort,
        shuffle: shuffle,
        boolval: boolval,
        intval: intval,
        floatval: floatval,
        strval: strval,
        empty: empty,
        isset: isset,
        is_array: is_array,
        is_bool: is_bool,
        is_float: is_float,
        is_int: is_int,
        is_integer: is_integer,
        is_null: is_null,
        is_numeric: is_numeric,
        is_object: is_object,
        is_string: is_string,
        is_callable: is_callable,
        date: date,
        time: time,
        microtime: microtime,
        strtotime: strtotime,
        mktime: mktime,
        getdate: getdate,
        str_pad: str_pad,
        nl2br: nl2br,
        strip_tags: strip_tags,
        stripslashes: stripslashes,
        addslashes: addslashes,
        htmlspecialchars: htmlspecialchars,
        wordwrap: wordwrap,
        ucfirst: ucfirst,
        lcfirst: lcfirst,
        ucwords: ucwords,
        strrev: strrev,
        crc32: crc32,
        hex2bin: hex2bin,
        bin2hex: bin2hex,
        str_rot13: str_rot13,
        levenshtein: levenshtein,
        soundex: soundex,
        metaphone: metaphone,
        deg2rad: deg2rad,
        rad2deg: rad2deg,
        max: max,
        min: min,
        abs: abs,
        ceil: ceil,
        floor: floor,
        round: round,
        sqrt: sqrt,
        pow: pow,
        exp: exp,
        log: log,
        sin: sin,
        cos: cos,
        tan: tan,
        asin: asin,
        acos: acos,
        atan: atan,
        atan2: atan2,
        hypot: hypot,
        pi: pi,
        rand: rand,
        mt_rand: mt_rand,
        getrandmax: getrandmax,
        mt_getrandmax: mt_getrandmax,
        array_rand: array_rand
    };
}

if (typeof window !== 'undefined') {
    window.Crypto = Crypto;
    window._ = _;
    window.load = load;
    window.$ = $;
    window.log = log;
    window.print = print;
    window.println = println;
    window.printLog = printLog;
    window.printDebug = printDebug;
    window.printError = printError;
    window.printInfo = printInfo;
    window.printWarn = printWarn;
    window.clear = clear;
    window.count = count;
    window.assert = assert;
    window.printTable = printTable;
    window.printTime = printTime;
    window.printTimeEnd = printTimeEnd;
    window.printTrace = printTrace;
    window.printGroup = printGroup;
    window.printGroupEnd = printGroupEnd;
    window.printGroupCollapsed = printGroupCollapsed;
    window.require = require;
    window.delay = delay;
    window.sleep = sleep;
    window.timeout = timeout;
    window.http_build_query = http_build_query;
    window.parse_str = parse_str;
    window.parse_url = parse_url;
    window.json_encode = json_encode;
    window.json_decode = json_decode;
    window.url_encode = url_encode;
    window.url_decode = url_decode;
    window.html_encode = html_encode;
    window.html_decode = html_decode;
    window.trim = trim;
    window.ltrim = ltrim;
    window.rtrim = rtrim;
    window.strtolower = strtolower;
    window.strtoupper = strtoupper;
    window.substr = substr;
    window.strlen = strlen;
    window.strpos = strpos;
    window.strrpos = strrpos;
    window.str_replace = str_replace;
    window.str_repeat = str_repeat;
    window.str_split = str_split;
    window.explode = explode;
    window.implode = implode;
    window.join = join;
    window.md5 = md5;
    window.sha1 = sha1;
    window.sha256 = sha256;
    window.base64_encode = base64_encode;
    window.base64_decode = base64_decode;
    window.urlencode = urlencode;
    window.urldecode = urldecode;
    window.rawurlencode = rawurlencode;
    window.rawurldecode = rawurldecode;
    window.number_format = number_format;
    window.sprintf = sprintf;
    window.printf = printf;
    window.in_array = in_array;
    window.array_keys = array_keys;
    window.array_values = array_values;
    window.array_merge = array_merge;
    window.array_push = array_push;
    window.array_pop = array_pop;
    window.array_shift = array_shift;
    window.array_unshift = array_unshift;
    window.array_slice = array_slice;
    window.array_splice = array_splice;
    window.array_reverse = array_reverse;
    window.array_sort = array_sort;
    window.array_unique = array_unique;
    window.array_search = array_search;
    window.array_key_exists = array_key_exists;
    window.count = count;
    window.sizeof = sizeof;
    window.range = range;
    window.array_chunk = array_chunk;
    window.array_filter = array_filter;
    window.array_map = array_map;
    window.sort = sort;
    window.rsort = rsort;
    window.ksort = ksort;
    window.shuffle = shuffle;
    window.boolval = boolval;
    window.intval = intval;
    window.floatval = floatval;
    window.strval = strval;
    window.empty = empty;
    window.isset = isset;
    window.is_array = is_array;
    window.is_bool = is_bool;
    window.is_float = is_float;
    window.is_int = is_int;
    window.is_integer = is_integer;
    window.is_null = is_null;
    window.is_numeric = is_numeric;
    window.is_object = is_object;
    window.is_string = is_string;
    window.is_callable = is_callable;
    window.date = date;
    window.time = time;
    window.microtime = microtime;
    window.strtotime = strtotime;
    window.mktime = mktime;
    window.getdate = getdate;
    window.str_pad = str_pad;
    window.nl2br = nl2br;
    window.strip_tags = strip_tags;
    window.stripslashes = stripslashes;
    window.addslashes = addslashes;
    window.htmlspecialchars = htmlspecialchars;
    window.wordwrap = wordwrap;
    window.ucfirst = ucfirst;
    window.lcfirst = lcfirst;
    window.ucwords = ucwords;
    window.strrev = strrev;
    window.crc32 = crc32;
    window.hex2bin = hex2bin;
    window.bin2hex = bin2hex;
    window.str_rot13 = str_rot13;
    window.levenshtein = levenshtein;
    window.soundex = soundex;
    window.metaphone = metaphone;
    window.deg2rad = deg2rad;
    window.rad2deg = rad2deg;
    window.max = max;
    window.min = min;
    window.abs = abs;
    window.ceil = ceil;
    window.floor = floor;
    window.round = round;
    window.sqrt = sqrt;
    window.pow = pow;
    window.exp = exp;
    window.log = log;
    window.sin = sin;
    window.cos = cos;
    window.tan = tan;
    window.asin = asin;
    window.acos = acos;
    window.atan = atan;
    window.atan2 = atan2;
    window.hypot = hypot;
    window.pi = pi;
    window.rand = rand;
    window.mt_rand = mt_rand;
    window.getrandmax = getrandmax;
    window.mt_getrandmax = mt_getrandmax;
    window.array_rand = array_rand;
}
