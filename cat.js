var CatAPI = {
    baseUrl: 'https://www.ylys.tv',
    apiUrl: 'https://www.ylys.tv/index.php',
    
    request: function(url, options) {
        options = options || {};
        options.type = options.type || 'GET';
        options.dataType = options.dataType || 'json';
        options.timeout = options.timeout || 30000;
        
        return new Promise(function(resolve, reject) {
            var xhr = new XMLHttpRequest();
            xhr.open(options.type, url, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.timeout = options.timeout;
            
            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        var response = JSON.parse(xhr.responseText);
                        resolve(response);
                    } catch(e) {
                        resolve(xhr.responseText);
                    }
                } else {
                    reject(new Error('Request failed with status: ' + xhr.status));
                }
            };
            
            xhr.onerror = function() {
                reject(new Error('Network error'));
            };
            
            xhr.ontimeout = function() {
                reject(new Error('Request timeout'));
            };
            
            if (options.data) {
                var params = [];
                for (var key in options.data) {
                    params.push(key + '=' + encodeURIComponent(options.data[key]));
                }
                xhr.send(params.join('&'));
            } else {
                xhr.send();
            }
        });
    },
    
    getHomePage: function(page, limit) {
        page = page || 1;
        limit = limit || 20;
        var url = this.apiUrl + '/api/vod/list?page=' + page + '&limit=' + limit;
        
        return this.request(url).then(function(response) {
            return response;
        });
    },
    
    getCategories: function() {
        var url = this.apiUrl + '/api/type/list';
        
        return this.request(url).then(function(response) {
            return response;
        });
    },
    
    getCategoryVideos: function(typeId, page, limit, params) {
        page = page || 1;
        limit = limit || 20;
        params = params || {};
        
        var data = {
            type: typeId,
            page: page,
            limit: limit
        };
        
        if (params.area) data.area = params.area;
        if (params.year) data.year = params.year;
        if (params.letter) data.letter = params.letter;
        if (params.order) data.order = params.order;
        if (params.by) data.by = params.by;
        if (params.class) data.class = params.class;
        
        var queryString = [];
        for (var key in data) {
            queryString.push(key + '=' + data[key]);
        }
        
        var url = this.apiUrl + '/api/vod/list?' + queryString.join('&');
        
        return this.request(url).then(function(response) {
            return response;
        });
    },
    
    getVideoDetail: function(vodId) {
        var url = this.apiUrl + '/api/vod/detail?id=' + vodId;
        
        return this.request(url).then(function(response) {
            return response;
        });
    },
    
    getVideoPlayer: function(id, sid, nid) {
        sid = sid || 1;
        nid = nid || 1;
        var url = this.apiUrl + '/ajax/player?id=' + id + '&sid=' + sid + '&nid=' + nid;
        
        return this.request(url).then(function(response) {
            return response;
        });
    },
    
    search: function(keyword, page, limit) {
        page = page || 1;
        limit = limit || 20;
        var url = this.apiUrl + '/api/vod/search?wd=' + encodeURIComponent(keyword) + '&page=' + page + '&limit=' + limit;
        
        return this.request(url).then(function(response) {
            return response;
        });
    },
    
    getRecommendVideos: function(limit) {
        limit = limit || 10;
        return this.getHomePage(1, limit).then(function(response) {
            if (response.list && response.list.length > 0) {
                return {
                    success: true,
                    data: response.list.slice(0, limit)
                };
            }
            return {
                success: false,
                message: 'No recommendations available'
            };
        });
    },
    
    getHotVideos: function(limit) {
        limit = limit || 10;
        return this.getCategoryVideos(1, 1, limit, {order: 'hits'}).then(function(response) {
            return response;
        });
    },
    
    getLatestVideos: function(limit) {
        limit = limit || 10;
        return this.getCategoryVideos(1, 1, limit, {order: 'time'}).then(function(response) {
            return response;
        });
    },
    
    buildCategoryUrl: function(typeId, params) {
        params = params || {};
        var url = this.baseUrl + '/vodshow/' + typeId;
        
        var segments = [
            params.area || '',
            params.year || '',
            params.letter || '',
            params.order || '',
            params.by || '',
            params.class || ''
        ];
        
        return url + '-' + segments.join('-') + '/';
    },
    
    buildDetailUrl: function(vodId) {
        return this.baseUrl + '/voddetail/' + vodId + '/';
    },
    
    buildPlayUrl: function(vodId, sid, nid) {
        sid = sid || 1;
        nid = nid || 1;
        return this.baseUrl + '/play/' + vodId + '-' + sid + '-' + nid + '/';
    },
    
    buildSearchUrl: function(keyword) {
        return this.baseUrl + '/vodsearch/' + encodeURIComponent(keyword) + '/';
    }
};

var CatUI = {
    createVideoCard: function(video, options) {
        options = options || {};
        var html = '<div class="video-card" style="' + (options.style || '') + '">';
        html += '<a href="' + (video.detail_url || CatAPI.buildDetailUrl(video.vod_id)) + '">';
        html += '<div class="video-cover">';
        html += '<img src="' + video.vod_pic + '" alt="' + video.vod_name + '" loading="lazy">';
        html += '<span class="video-tag">' + (video.vod_remarks || '') + '</span>';
        html += '</div>';
        html += '<div class="video-info">';
        html += '<h3 class="video-title">' + video.vod_name + '</h3>';
        html += '<p class="video-subtitle">' + (video.vod_sub || '') + '</p>';
        html += '</div>';
        html += '</a>';
        html += '</div>';
        return html;
    },
    
    createCategoryList: function(categories) {
        var html = '<div class="category-list">';
        if (categories && categories.length > 0) {
            for (var i = 0; i < categories.length; i++) {
                var cat = categories[i];
                html += '<a href="' + CatAPI.buildCategoryUrl(cat.type_id) + '" class="category-item">';
                html += '<span class="category-icon">' + (cat.type_icon || '📁') + '</span>';
                html += '<span class="category-name">' + cat.type_name + '</span>';
                html += '</a>';
            }
        }
        html += '</div>';
        return html;
    },
    
    createVideoGrid: function(videos, options) {
        options = options || {};
        var html = '<div class="video-grid" style="display:grid;grid-template-columns:repeat(auto-fill,minmax(' + (options.columnWidth || '200px') + ',1fr));gap:' + (options.gap || '20px') + ';padding:' + (options.padding || '20px') + ';">';
        if (videos && videos.length > 0) {
            for (var i = 0; i < videos.length; i++) {
                html += this.createVideoCard(videos[i], {
                    style: 'cursor:pointer;transition:transform 0.3s;'
                });
            }
        }
        html += '</div>';
        return html;
    },
    
    createPagination: function(currentPage, totalPages, onPageChange) {
        var html = '<div class="pagination" style="display:flex;justify-content:center;gap:10px;padding:20px;">';
        
        if (currentPage > 1) {
            html += '<button class="page-btn" data-page="' + (currentPage - 1) + '">上一页</button>';
        }
        
        var startPage = Math.max(1, currentPage - 2);
        var endPage = Math.min(totalPages, currentPage + 2);
        
        for (var i = startPage; i <= endPage; i++) {
            var active = i === currentPage ? 'background:#007bff;color:#fff;' : '';
            html += '<button class="page-btn" data-page="' + i + '" style="' + active + '">' + i + '</button>';
        }
        
        if (currentPage < totalPages) {
            html += '<button class="page-btn" data-page="' + (currentPage + 1) + '">下一页</button>';
        }
        
        html += '</div>';
        return html;
    },
    
    createSearchBar: function(containerId, options) {
        options = options || {};
        var container = document.getElementById(containerId);
        if (!container) {
            console.error('Search container not found:', containerId);
            return;
        }
        
        var html = '<div class="search-bar" style="display:flex;gap:10px;padding:10px;">';
        html += '<input type="text" class="search-input" placeholder="' + (options.placeholder || '搜索视频...') + '" style="flex:1;padding:10px;border:1px solid #ddd;border-radius:4px;">';
        html += '<button class="search-btn" style="padding:10px 20px;background:#007bff;color:#fff;border:none;border-radius:4px;cursor:pointer;">搜索</button>';
        html += '</div>';
        
        container.innerHTML = html;
        
        var input = container.querySelector('.search-input');
        var button = container.querySelector('.search-btn');
        
        var searchHandler = function() {
            var keyword = input.value.trim();
            if (keyword && options.onSearch) {
                options.onSearch(keyword);
            }
        };
        
        button.onclick = searchHandler;
        input.onkeypress = function(e) {
            if (e.key === 'Enter') {
                searchHandler();
            }
        };
    },
    
    createHomePage: function(containerId, options) {
        options = options || {};
        var container = document.getElementById(containerId);
        if (!container) {
            console.error('Home container not found:', containerId);
            return;
        }
        
        var self = this;
        
        container.innerHTML = '<div class="loading" style="text-align:center;padding:50px;">加载中...</div>';
        
        CatAPI.getRecommendVideos(options.limit || 12).then(function(result) {
            if (result.success && result.data) {
                var html = '<div class="home-page">';
                html += '<div class="section-title" style="font-size:24px;font-weight:bold;padding:20px;">热门推荐</div>';
                html += self.createVideoGrid(result.data, options.gridOptions);
                html += '</div>';
                container.innerHTML = html;
                
                if (options.onVideoClick) {
                    var cards = container.querySelectorAll('.video-card');
                    cards.forEach(function(card, index) {
                        card.onclick = function() {
                            options.onVideoClick(result.data[index]);
                        };
                    });
                }
            } else {
                container.innerHTML = '<div class="error" style="text-align:center;padding:50px;color:#999;">暂无推荐内容</div>';
            }
        }).catch(function(error) {
            container.innerHTML = '<div class="error" style="text-align:center;padding:50px;color:#999;">加载失败: ' + error.message + '</div>';
        });
    },
    
    createCategoryPage: function(containerId, typeId, options) {
        options = options || {};
        var container = document.getElementById(containerId);
        if (!container) {
            console.error('Category container not found:', containerId);
            return;
        }
        
        var self = this;
        var currentPage = 1;
        var totalPages = 1;
        
        container.innerHTML = '<div class="loading" style="text-align:center;padding:50px;">加载中...</div>';
        
        function loadVideos(page) {
            CatAPI.getCategoryVideos(typeId, page, options.limit || 20, options.params || {}).then(function(result) {
                if (result.list && result.list.length > 0) {
                    totalPages = result.pagecount || 1;
                    currentPage = result.page || page;
                    
                    var html = '<div class="category-page">';
                    html += '<div class="section-title" style="font-size:24px;font-weight:bold;padding:20px;">' + (options.title || '分类内容') + '</div>';
                    html += self.createVideoGrid(result.list, options.gridOptions);
                    html += self.createPagination(currentPage, totalPages);
                    html += '</div>';
                    container.innerHTML = html;
                    
                    var pageButtons = container.querySelectorAll('.page-btn');
                    pageButtons.forEach(function(btn) {
                        btn.onclick = function() {
                            var pageNum = parseInt(this.getAttribute('data-page'));
                            loadVideos(pageNum);
                        };
                    });
                    
                    if (options.onVideoClick) {
                        var cards = container.querySelectorAll('.video-card');
                        cards.forEach(function(card, index) {
                            card.onclick = function() {
                                options.onVideoClick(result.list[index]);
                            };
                        });
                    }
                } else {
                    container.innerHTML = '<div class="empty" style="text-align:center;padding:50px;color:#999;">该分类暂无内容</div>';
                }
            }).catch(function(error) {
                container.innerHTML = '<div class="error" style="text-align:center;padding:50px;color:#999;">加载失败: ' + error.message + '</div>';
            });
        }
        
        loadVideos(1);
    },
    
    createSearchPage: function(containerId, keyword, options) {
        options = options || {};
        var container = document.getElementById(containerId);
        if (!container) {
            console.error('Search container not found:', containerId);
            return;
        }
        
        var self = this;
        var currentPage = 1;
        var totalPages = 1;
        
        container.innerHTML = '<div class="loading" style="text-align:center;padding:50px;">搜索"' + keyword + '"...</div>';
        
        function loadSearchResults(page) {
            CatAPI.search(keyword, page, options.limit || 20).then(function(result) {
                if (result.list && result.list.length > 0) {
                    totalPages = result.pagecount || 1;
                    currentPage = result.page || page;
                    
                    var html = '<div class="search-page">';
                    html += '<div class="section-title" style="font-size:24px;font-weight:bold;padding:20px;">搜索结果: "' + keyword + '" (共' + result.total + '条)</div>';
                    html += self.createVideoGrid(result.list, options.gridOptions);
                    html += self.createPagination(currentPage, totalPages);
                    html += '</div>';
                    container.innerHTML = html;
                    
                    var pageButtons = container.querySelectorAll('.page-btn');
                    pageButtons.forEach(function(btn) {
                        btn.onclick = function() {
                            var pageNum = parseInt(this.getAttribute('data-page'));
                            loadSearchResults(pageNum);
                        };
                    });
                    
                    if (options.onVideoClick) {
                        var cards = container.querySelectorAll('.video-card');
                        cards.forEach(function(card, index) {
                            card.onclick = function() {
                                options.onVideoClick(result.list[index]);
                            };
                        });
                    }
                } else {
                    container.innerHTML = '<div class="empty" style="text-align:center;padding:50px;color:#999;">未找到"' + keyword + '"相关视频</div>';
                }
            }).catch(function(error) {
                container.innerHTML = '<div class="error" style="text-align:center;padding:50px;color:#999;">搜索失败: ' + error.message + '</div>';
            });
        }
        
        loadSearchResults(1);
    }
};

var CatRouter = {
    routes: {},
    currentRoute: null,
    
    init: function() {
        var self = this;
        
        window.onpopstate = function() {
            self.handleRoute();
        };
        
        this.handleRoute();
    },
    
    addRoute: function(path, handler) {
        this.routes[path] = handler;
    },
    
    navigate: function(path) {
        history.pushState(null, '', path);
        this.handleRoute();
    },
    
    handleRoute: function() {
        var path = window.location.pathname;
        
        for (var route in this.routes) {
            var match = path.match(new RegExp('^' + route.replace(/:[^/]+/g, '([^/]+)') + '$'));
            if (match) {
                this.currentRoute = route;
                var params = match.slice(1);
                this.routes[route].apply(this, params);
                return;
            }
        }
        
        if (this.routes['*']) {
            this.routes['*']();
        }
    }
};

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
    module.exports = {
        CatPlayer: CatPlayer,
        CatAPI: CatAPI,
        CatUI: CatUI,
        CatRouter: CatRouter
    };
} else if (typeof window !== 'undefined') {
    window.CatPlayer = CatPlayer;
    window.CatAPI = CatAPI;
    window.CatUI = CatUI;
    window.CatRouter = CatRouter;
}
