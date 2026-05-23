var CatPlayer = {
    base64EncodeChars: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
    base64DecodeChars: new Array(-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,62,-1,-1,-1,63,52,53,54,55,56,57,58,59,60,61,-1,-1,-1,-1,-1,-1,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,-1,-1,-1,-1,-1,-1,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1,-1),
    
    base64encode: function(str) {
        var out, i, len, c1, c2, c3;
        len = str.length;
        i = 0;
        out = "";
        while(i < len) {
            c1 = str.charCodeAt(i++) & 0xff;
            if(i == len) {
                out += this.base64EncodeChars.charAt(c1 >> 2);
                out += this.base64EncodeChars.charAt((c1 & 0x3) << 4);
                out += "==";
                break;
            }
            c2 = str.charCodeAt(i++);
            if(i == len) {
                out += this.base64EncodeChars.charAt(c1 >> 2);
                out += this.base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
                out += this.base64EncodeChars.charAt((c2 & 0xF) << 2);
                out += "=";
                break;
            }
            c3 = str.charCodeAt(i++);
            out += this.base64EncodeChars.charAt(c1 >> 2);
            out += this.base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
            out += this.base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
            out += this.base64EncodeChars.charAt(c3 & 0x3F);
        }
        return out;
    },
    
    base64decode: function(str) {
        var c1, c2, c3, c4, i, len, out;
        len = str.length;
        i = 0;
        out = "";
        while(i < len) {
            do {
                c1 = this.base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while(i < len && c1 == -1);
            if(c1 == -1) break;
            
            do {
                c2 = this.base64DecodeChars[str.charCodeAt(i++) & 0xff];
            } while(i < len && c2 == -1);
            if(c2 == -1) break;
            
            out += String.fromCharCode((c1 << 2) | ((c2 & 0x30) >> 4));
            
            do {
                c3 = str.charCodeAt(i++) & 0xff;
                if(c3 == 61) return out;
                c3 = this.base64DecodeChars[c3];
            } while(i < len && c3 == -1);
            if(c3 == -1) break;
            
            out += String.fromCharCode(((c2 & 0XF) << 4) | ((c3 & 0x3C) >> 2));
            
            do {
                c4 = str.charCodeAt(i++) & 0xff;
                if(c4 == 61) return out;
                c4 = this.base64DecodeChars[c4];
            } while(i < len && c4 == -1);
            if(c4 == -1) break;
            
            out += String.fromCharCode(((c3 & 0x03) << 6) | c4);
        }
        return out;
    },
    
    utf16to8: function(str) {
        var out, i, len, c;
        out = "";
        len = str.length;
        for(i = 0; i < len; i++) {
            c = str.charCodeAt(i);
            if((c >= 0x0001) && (c <= 0x007F)) {
                out += str.charAt(i);
            } else if(c > 0x07FF) {
                out += String.fromCharCode(0xE0 | ((c >> 12) & 0x0F));
                out += String.fromCharCode(0x80 | ((c >> 6) & 0x3F));
                out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            } else {
                out += String.fromCharCode(0xC0 | ((c >> 6) & 0x1F));
                out += String.fromCharCode(0x80 | ((c >> 0) & 0x3F));
            }
        }
        return out;
    },
    
    utf8to16: function(str) {
        var out, i, len, c, char2, char3;
        out = "";
        len = str.length;
        i = 0;
        while(i < len) {
            c = str.charCodeAt(i++);
            switch(c >> 4) {
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
    },
    
    decryptUrl: function(encryptedUrl, encryptType) {
        if (!encryptedUrl) return '';
        
        switch(encryptType) {
            case '1':
                return unescape(encryptedUrl);
            case '2':
                return unescape(this.base64decode(encryptedUrl));
            case '0':
            default:
                return encryptedUrl;
        }
    },
    
    encryptUrl: function(url, encryptType) {
        if (!url) return '';
        
        switch(encryptType) {
            case '1':
                return escape(url);
            case '2':
                return this.base64encode(unescape(encodeURIComponent(url)));
            case '0':
            default:
                return url;
        }
    },
    
    getDate: function(format, date) {
        if (!date) {
            date = new Date();
        }
        var Week = ['日', '一', '二', '三', '四', '五', '六'];
        format = format.replace(/yyyy|YYYY/, date.getFullYear());
        format = format.replace(/yy|YY/, (date.getYear() % 100) > 9 ? (date.getYear() % 100).toString() : '0' + (date.getYear() % 100));
        format = format.replace(/MM/, date.getMonth() > 9 ? date.getMonth().toString() : '0' + date.getMonth());
        format = format.replace(/M/g, date.getMonth());
        format = format.replace(/w|W/g, Week[date.getDay()]);
        format = format.replace(/dd|DD/, date.getDate() > 9 ? date.getDate().toString() : '0' + date.getDate());
        format = format.replace(/d|D/g, date.getDate());
        format = format.replace(/hh|HH/, date.getHours() > 9 ? date.getHours().toString() : '0' + date.getHours());
        format = format.replace(/h|H/g, date.getHours());
        format = format.replace(/mm/, date.getMinutes() > 9 ? date.getMinutes().toString() : '0' + date.getMinutes());
        format = format.replace(/m/g, date.getMinutes());
        format = format.replace(/ss|SS/, date.getSeconds() > 9 ? date.getSeconds().toString() : '0' + date.getSeconds());
        format = format.replace(/s|S/g, date.getSeconds());
        return format;
    },
    
    buildPlayerUrl: function(template, sid, nid) {
        return template.replace(/\{sid\}/g, sid).replace(/\{nid\}/g, nid);
    },
    
    detectMobile: function() {
        var agent = navigator.userAgent.toLowerCase();
        return agent.indexOf("android") > 0 || 
               agent.indexOf("mobile") > 0 || 
               agent.indexOf("ipod") > 0 || 
               agent.indexOf("ios") > 0 || 
               agent.indexOf("iphone") > 0 || 
               agent.indexOf("ipad") > 0;
    },
    
    getPlayerConfig: function(config) {
        return {
            width: this.detectMobile() ? (config.widthmob || '100%') : (config.width || '100%'),
            height: this.detectMobile() ? (config.heightmob || '100%') : (config.height || '100%'),
            prestrain: config.prestrain || '',
            buffer: config.buffer || '',
            second: config.second || 0,
            parse: config.parse || '',
            server_list: config.server_list || {},
            player_list: config.player_list || {}
        };
    },
    
    parsePlayerData: function(playerData) {
        var decryptUrl = this.decryptUrl.bind(this);
        
        if (playerData.encrypt == '1') {
            playerData.url = decryptUrl(playerData.url, '1');
            playerData.url_next = decryptUrl(playerData.url_next, '1');
        } else if (playerData.encrypt == '2') {
            playerData.url = decryptUrl(playerData.url, '2');
            playerData.url_next = decryptUrl(playerData.url_next, '2');
        }
        
        return playerData;
    },
    
    createVideoPlayer: function(containerId, videoUrl, options) {
        options = options || {};
        var container = document.getElementById(containerId);
        if (!container) {
            console.error('Container not found:', containerId);
            return null;
        }
        
        var width = options.width || '100%';
        var height = options.height || '100%';
        
        var html = '<div style="width:' + width + ';height:' + height + ';background:#000;">';
        html += '<video width="100%" height="100%" controls autoplay>';
        html += '<source src="' + videoUrl + '" type="video/mp4">';
        html += 'Your browser does not support the video tag.';
        html += '</video>';
        html += '</div>';
        
        container.innerHTML = html;
        return container.querySelector('video');
    },
    
    createIframePlayer: function(containerId, playerUrl, options) {
        options = options || {};
        var container = document.getElementById(containerId);
        if (!container) {
            console.error('Container not found:', containerId);
            return null;
        }
        
        var width = options.width || '100%';
        var height = options.height || '100%';
        
        var iframe = document.createElement('iframe');
        iframe.width = width;
        iframe.height = height;
        iframe.frameBorder = '0';
        iframe.src = playerUrl;
        iframe.setAttribute('allowfullscreen', 'allowfullscreen');
        iframe.setAttribute('mozallowfullscreen', 'mozallowfullscreen');
        iframe.setAttribute('msallowfullscreen', 'msallowfullscreen');
        iframe.setAttribute('oallowfullscreen', 'oallowfullscreen');
        iframe.setAttribute('webkitallowfullscreen', 'webkitallowfullscreen');
        
        container.innerHTML = '';
        container.appendChild(iframe);
        return iframe;
    },
    
    init: function(playerData, containerId, options) {
        var parsedData = this.parsePlayerData(playerData);
        var self = this;
        
        if (parsedData.from === 'parse') {
            var parseUrl = (options.parseUrl || '') + parsedData.url;
            return this.createIframePlayer(containerId, parseUrl, options);
        } else {
            return this.createVideoPlayer(containerId, parsedData.url, options);
        }
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = CatPlayer;
}
