
// 这是一个简单的测试脚本，模拟我们的解析逻辑
const fs = require('fs');

// 模拟 cheerio 的 $ 函数
function $(html) {
    this.html = html;
    
    this.find = function(selector) {
        // 简单的模拟，实际应该使用 cheerio
        return {
            each: function(callback) {
                // 查找所有 li 标签
                const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/g;
                let match;
                let index = 0;
                while ((match = liRegex.exec(html)) !== null) {
                    callback(index, {
                        html: match[1],
                        find: function(sel) {
                            if (sel.indexOf('a[href*="/vod-detail-id-"]') !== -1) {
                                const aRegex = /<a[^>]*href="([^"]*vod-detail-id-[^"]*)"[^>]*>/;
                                const aMatch = match[1].match(aRegex);
                                if (aMatch) {
                                    return {
                                        length: 1,
                                        attr: function(name) {
                                            if (name === 'href') return aMatch[1];
                                            if (name === 'title') {
                                                const titleMatch = aMatch[0].match(/title="([^"]*)"/);
                                                return titleMatch ? titleMatch[1] : '';
                                            }
                                            return '';
                                        },
                                        first: function() { return this; }
                                    };
                                }
                            }
                            if (sel.indexOf('img') !== -1) {
                                const imgRegex = /<img[^>]*>/;
                                const imgMatch = match[1].match(imgRegex);
                                if (imgMatch) {
                                    return {
                                        length: 1,
                                        attr: function(name) {
                                            if (name === 'data-src') {
                                                const dsMatch = imgMatch[0].match(/data-src="([^"]*)"/);
                                                return dsMatch ? dsMatch[1] : '';
                                            }
                                            if (name === 'src') {
                                                const srcMatch = imgMatch[0].match(/src="([^"]*)"/);
                                                return srcMatch ? srcMatch[1] : '';
                                            }
                                            return '';
                                        },
                                        first: function() { return this; }
                                    };
                                }
                            }
                            if (sel.indexOf('.sTit') !== -1) {
                                const sTitRegex = /<span[^>]*class="[^"]*sTit[^"]*"[^>]*>([^<]*)<\/span>/;
                                const sTitMatch = match[1].match(sTitRegex);
                                if (sTitMatch) {
                                    return {
                                        length: 1,
                                        text: function() { return sTitMatch[1]; }
                                    };
                                }
                            }
                            return { length: 0 };
                        },
                        text: function() {
                            return match[1].replace(/<[^>]*>/g, '');
                        }
                    });
                    index++;
                }
            }
        };
    };
    
    return this;
}

// 模拟 fixUrl 函数
function fixUrl(url) {
    if (!url) return '';
    if (url.startsWith('//')) {
        return 'https:' + url;
    }
    return url;
}

// 复制我们更新后的 parseVodList 函数
function parseVodList($obj, selector) {
    const list = [];
    
    const html = $obj.html;
    
    // 简单的模拟选择器 #data_list li
    if (selector === '#data_list li') {
        const dataListStart = html.indexOf('id="data_list"');
        if (dataListStart !== -1) {
            // 找到 data_list 区域
            const ulStart = html.lastIndexOf('<ul', dataListStart);
            const ulEnd = html.indexOf('</ul>', ulStart);
            const ulHtml = html.substring(ulStart, ulEnd + 5);
            
            // 解析每个 li
            const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/g;
            let match;
            let index = 0;
            while ((match = liRegex.exec(ulHtml)) !== null) {
                const liHtml = match[1];
                
                // 查找链接
                let href = '';
                const aRegex = /<a[^>]*href="([^"]*)"[^>]*>/g;
                let aMatch;
                while ((aMatch = aRegex.exec(liHtml)) !== null) {
                    if (aMatch[1].indexOf('vod-detail-id') !== -1) {
                        href = aMatch[1];
                        break;
                    }
                }
                
                if (!href) continue;
                
                // 提取 ID
                const vodIdMatch = href.match(/vod-detail-id-(\d+)/);
                if (!vodIdMatch) continue;
                const vodId = vodIdMatch[1];
                
                // 获取图片
                let vodPic = '';
                const imgRegex = /<img[^>]*>/;
                const imgMatch = liHtml.match(imgRegex);
                if (imgMatch) {
                    const dataSrcMatch = imgMatch[0].match(/data-src="([^"]*)"/);
                    if (dataSrcMatch) {
                        vodPic = dataSrcMatch[1];
                    } else {
                        const srcMatch = imgMatch[0].match(/src="([^"]*)"/);
                        if (srcMatch) {
                            vodPic = srcMatch[1];
                        }
                    }
                }
                vodPic = fixUrl(vodPic);
                
                // 获取标题
                let vodName = '';
                const sTitRegex = /<span[^>]*class="[^"]*sTit[^"]*"[^>]*>([^<]*)<\/span>/;
                const sTitMatch = liHtml.match(sTitRegex);
                if (sTitMatch) {
                    vodName = sTitMatch[1].trim();
                }
                
                list.push({
                    vod_id: vodId,
                    vod_name: vodName,
                    vod_pic: vodPic,
                    vod_remarks: ''
                });
            }
        }
    }
    
    return list;
}

// 测试解析搜索结果
try {
    const searchHtml = fs.readFileSync('/workspace/yulinling_search.html', 'utf-8');
    const $search = $(searchHtml);
    const results = parseVodList($search, '#data_list li');
    
    console.log('解析到 ' + results.length + ' 个搜索结果：');
    results.forEach((item, index) => {
        console.log('\n结果 ' + (index + 1) + ':');
        console.log('ID: ' + item.vod_id);
        console.log('名称: ' + item.vod_name);
        console.log('图片: ' + item.vod_pic);
    });
    
    if (results.length > 0) {
        console.log('\n✅ 解析成功！');
    } else {
        console.log('\n❌ 没有解析到任何结果');
    }
} catch (e) {
    console.error('测试出错:', e);
}
