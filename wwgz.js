import { Crypto, load, _ } from 'assets://js/lib/cat.js';

let key = 'wwgz';
let HOST = 'https://vip.wwgz.cn:5200';
let parseMap = {};
let siteKey = '';
let siteType = 0;

const UAMobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1';

async function request(reqUrl, postData = null) {
    let res;
    if (postData) {
        res = await req(reqUrl, {
            method: 'post',
            headers: {
                'User-Agent': UAMobile,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data: postData,
        });
    } else {
        res = await req(reqUrl, {
            method: 'get',
            headers: {
                'User-Agent': UAMobile,
            },
        });
    }
    return res.content;
}

async function init(cfg) {
    siteKey = cfg.skey;
    siteType = cfg.stype;
}

async function home(filter) {
    const classes = [
        {'type_id':'1','type_name':'电影'},
        {'type_id':'2','type_name':'连续剧'},
        {'type_id':'3','type_name':'综艺'},
        {'type_id':'4','type_name':'动漫'},
        {'type_id':'26','type_name':'短剧'},
        {'type_id':'20','type_name':'小姐姐'},
        {'type_id':'31','type_name':'音乐'}
    ];
    
    const filterObj = {
        '1': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            },
            {
                'key': 'area',
                'name': '地区',
                'value': [
                    {'n':'全部','v':''},
                    {'n':'大陆','v':'大陆'},
                    {'n':'香港','v':'香港'},
                    {'n':'台湾','v':'台湾'},
                    {'n':'美国','v':'美国'},
                    {'n':'韩国','v':'韩国'},
                    {'n':'日本','v':'日本'},
                    {'n':'泰国','v':'泰国'},
                    {'n':'新加坡','v':'新加坡'},
                    {'n':'马来西亚','v':'马来西亚'},
                    {'n':'英国','v':'英国'},
                    {'n':'法国','v':'法国'},
                    {'n':'其它','v':'其它'}
                ]
            },
            {
                'key': 'year',
                'name': '年代',
                'value': [
                    {'n':'全部','v':'0'},
                    {'n':'2026','v':'2026'},
                    {'n':'2025','v':'2025'},
                    {'n':'2024','v':'2024'},
                    {'n':'2023','v':'2023'},
                    {'n':'2022','v':'2022'},
                    {'n':'2021','v':'2021'},
                    {'n':'2020','v':'2020'},
                    {'n':'2019','v':'2019'},
                    {'n':'2018','v':'2018'}
                ]
            }
        ],
        '2': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            },
            {
                'key': 'area',
                'name': '地区',
                'value': [
                    {'n':'全部','v':''},
                    {'n':'大陆','v':'大陆'},
                    {'n':'香港','v':'香港'},
                    {'n':'台湾','v':'台湾'},
                    {'n':'美国','v':'美国'},
                    {'n':'韩国','v':'韩国'},
                    {'n':'日本','v':'日本'}
                ]
            },
            {
                'key': 'year',
                'name': '年代',
                'value': [
                    {'n':'全部','v':'0'},
                    {'n':'2026','v':'2026'},
                    {'n':'2025','v':'2025'},
                    {'n':'2024','v':'2024'},
                    {'n':'2023','v':'2023'},
                    {'n':'2022','v':'2022'},
                    {'n':'2021','v':'2021'}
                ]
            }
        ],
        '3': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            }
        ],
        '4': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            },
            {
                'key': 'area',
                'name': '地区',
                'value': [
                    {'n':'全部','v':''},
                    {'n':'大陆','v':'大陆'},
                    {'n':'日本','v':'日本'},
                    {'n':'美国','v':'美国'}
                ]
            }
        ],
        '26': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            }
        ],
        '20': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            }
        ],
        '31': [
            {
                'key': 'by',
                'name': '排序',
                'value': [
                    {'n':'时间','v':'time'},
                    {'n':'人气','v':'hits'},
                    {'n':'评分','v':'score'}
                ]
            }
        ]
    };
    
    return JSON.stringify({
        class: classes,
        filters: filterObj,
    });
}

async function homeVod() {
    const html = await request(HOST + '/');
    const $ = load(html);
    const videos = [];
    
    $('section.mod li').each((i, li) => {
        const $li = $(li);
        const $a = $li.find('a[href*="/vod-detail-id-"]');
        if ($a.length > 0) {
            const href = $a.attr('href');
            const id = href.match(/\/vod-detail-id-(\d+)\.html/)?.[1];
            
            if (id && videos.filter(v => v.vod_id === id).length === 0) {
                let vodPic = $li.find('img').attr('data-src') || 
                            $li.find('img').attr('data-echo') || 
                            $li.find('img').attr('src') || '';
                
                if (vodPic && !vodPic.startsWith('http')) {
                    if (vodPic.startsWith('//')) {
                        vodPic = 'https:' + vodPic;
                    } else if (vodPic.startsWith('/')) {
                        vodPic = HOST + vodPic;
                    }
                }
                
                const title = $a.attr('title') || $li.find('.sTit').text().trim() || '';
                const remarks = $li.find('.sDes').text().trim() || '';
                
                if (title && !title.includes('logo') && !title.includes('搜索')) {
                    videos.push({
                        vod_id: id,
                        vod_name: title,
                        vod_pic: vodPic,
                        vod_remarks: remarks,
                    });
                }
            }
        }
    });
    
    return JSON.stringify({
        list: videos.slice(0, 40),
    });
}

async function category(tid, pg, filter, extend) {
    if (pg <= 0) pg = 1;
    
    const by = extend.by || 'time';
    const area = extend.area || '';
    const year = extend.year || '0';
    const letter = extend.letter || '';
    
    const link = HOST + '/index.php?m=vod-list-id-' + tid + '-pg-' + pg + '-order--by-' + by + '-class-0-year-' + year + '-letter-' + letter + '-area-' + encodeURIComponent(area) + '-lang-.html';
    
    const html = await request(link);
    const $ = load(html);
    const videos = [];
    
    $('ul.resize_list li').each((i, li) => {
        const $li = $(li);
        const $a = $li.find('a[href*="/vod-detail-id-"]');
        if ($a.length > 0) {
            const href = $a.attr('href');
            const id = href.match(/\/vod-detail-id-(\d+)\.html/)?.[1];
            
            if (id) {
                let vodPic = $li.find('img').attr('data-src') || 
                            $li.find('img').attr('data-echo') || 
                            $li.find('img').attr('src') || '';
                
                if (vodPic && !vodPic.startsWith('http')) {
                    if (vodPic.startsWith('//')) {
                        vodPic = 'https:' + vodPic;
                    } else if (vodPic.startsWith('/')) {
                        vodPic = HOST + vodPic;
                    }
                }
                
                const title = $a.attr('title') || $li.find('.sTit').text().trim() || '';
                const remarks = $li.find('.sDes').text().trim() || '';
                
                if (title) {
                    videos.push({
                        vod_id: id,
                        vod_name: title,
                        vod_pic: vodPic,
                        vod_remarks: remarks,
                    });
                }
            }
        }
    });
    
    let total = 0;
    let pageCount = 1;
    
    const pageText = $('div.page').text();
    const totalMatch = pageText.match(/共(\d+)条数据/);
    const pageMatch = pageText.match(/当前:(\d+)\/(\d+)页/);
    
    if (totalMatch) {
        total = parseInt(totalMatch[1]);
        pageCount = Math.ceil(total / 30);
    }
    
    if (pageMatch) {
        pageCount = parseInt(pageMatch[2]);
    }
    
    return JSON.stringify({
        page: parseInt(pg),
        pagecount: pageCount,
        limit: 30,
        total: total,
        list: videos,
    });
}

async function detail(id) {
    const html = await request(HOST + '/vod-detail-id-' + id + '.html');
    const $ = load(html);
    
    const $img = $('section.page-hd img');
    let vodPic = $img.attr('src') || '';
    if (vodPic && !vodPic.startsWith('http')) {
        if (vodPic.startsWith('//')) {
            vodPic = 'https:' + vodPic;
        } else if (vodPic.startsWith('/')) {
            vodPic = HOST + vodPic;
        }
    }
    
    const title = $('h1.title').text().trim() || $('section.page-hd a').attr('title') || '';
    
    const $descItems = $('div.desc_item');
    let vod_actor = '';
    let vod_director = '';
    let vod_year = '';
    
    $descItems.each((i, item) => {
        const text = $(item).text();
        if (text.includes('主演')) {
            vod_actor = text.replace('主演:', '').replace(/<[^>]+>/g, '').trim();
        } else if (text.includes('导演')) {
            vod_director = text.replace('导演:', '').replace(/<[^>]+>/g, '').trim();
        } else if (text.includes('年代')) {
            vod_year = text.match(/(\d{4})/)?.[1] || '';
        }
    });
    
    const vod_content = $('article.detail-con p').text().trim() || '';
    
    let macFrom = '';
    let macUrl = '';
    const $scripts = $('script');
    $scripts.each((i, script) => {
        const text = $(script).html() || '';
        if (text.includes('mac_from=')) {
            const match = text.match(/mac_from\s*=\s*['"]([^'"]+)['"]/);
            if (match) macFrom = match[1];
        }
        if (text.includes('mac_url=')) {
            const match = text.match(/mac_url\s*=\s*['"]([^'"]+)['"]/);
            if (match) macUrl = match[1];
        }
    });
    
    parseMap[id] = { macFrom, macUrl };
    
    const playMap = {};
    $('div.numList').each((idx, list) => {
        const $list = $(list);
        const $tabs = $list.prev('.hd ul li');
        let fromName = $tabs.eq(idx).text().trim() || '线路' + (idx + 1);
        
        $list.find('li a').each((i, item) => {
            const $item = $(item);
            const epTitle = $item.text().trim();
            const epUrl = $item.attr('href') || '';
            
            if (!playMap.hasOwnProperty(fromName)) {
                playMap[fromName] = [];
            }
            playMap[fromName].push(epTitle + '$' + epUrl);
        });
    });
    
    const vod_play_from = _.keys(playMap).join('$$$');
    const vod_play_url = _.values(playMap).map(list => list.join('#')).join('$$$');
    
    const vod = {
        vod_id: id,
        vod_name: title,
        vod_pic: vodPic,
        vod_actor: vod_actor.replace(/<[^>]+>/g, ''),
        vod_director: vod_director.replace(/<[^>]+>/g, ''),
        vod_year: vod_year,
        vod_content: vod_content,
        vod_play_from: vod_play_from,
        vod_play_url: vod_play_url,
    };
    
    return JSON.stringify({
        list: [vod],
    });
}

async function play(flag, id, flags) {
    const idMatch = id.match(/vod-detail-id-(\d+)/);
    const vodId = idMatch ? idMatch[1] : '';
    
    let macFrom = '';
    let macUrl = '';
    
    if (vodId && parseMap[vodId]) {
        macFrom = parseMap[vodId].macFrom || '';
        macUrl = parseMap[vodId].macUrl || '';
    }
    
    if (!macUrl) {
        const html = await request(HOST + id);
        const $ = load(html);
        
        const $scripts = $('script');
        $scripts.each((i, script) => {
            const text = $(script).html() || '';
            if (text.includes('mac_from=')) {
                const match = text.match(/mac_from\s*=\s*['"]([^'"]+)['"]/);
                if (match) macFrom = match[1];
            }
            if (text.includes('mac_url=')) {
                const match = text.match(/mac_url\s*=\s*['"]([^'"]+)['"]/);
                if (match) macUrl = match[1];
            }
        });
    }
    
    const srcMatch = id.match(/src-(\d+)-/);
    const srcNum = srcMatch ? parseInt(srcMatch[1]) : 1;
    
    const urlParts = macUrl.split('$$$');
    const fromParts = macFrom.split('$$$');
    
    let encryptUrl = '';
    let encodeType = '';
    
    if (srcNum === 2 && urlParts.length >= 2) {
        const line2Data = urlParts[1];
        const line2Eps = line2Data.split('#');
        const currentEp = line2Eps.find(ep => ep.includes('$'));
        if (currentEp) {
            encryptUrl = currentEp.split('$')[1] || currentEp;
        }
        encodeType = fromParts.length >= 2 ? fromParts[1] : '';
    } else {
        const line1Data = urlParts[0];
        const line1Eps = line1Data.split('#');
        const currentEp = line1Eps.find(ep => ep.includes('$'));
        if (currentEp) {
            encryptUrl = currentEp.split('$')[1] || currentEp;
        }
        encodeType = fromParts.length >= 1 ? fromParts[0] : '';
    }
    
    let videoUrl = decryptVideoUrl(encryptUrl, encodeType, srcNum);
    
    if (!videoUrl) {
        videoUrl = 'https://api.nmvod.me:520/player/?url=' + encodeURIComponent(encryptUrl);
        return JSON.stringify({
            parse: 1,
            url: videoUrl,
            header: {
                'User-Agent': UAMobile,
                'Referer': HOST + '/',
            }
        });
    }
    
    return JSON.stringify({
        parse: 0,
        url: videoUrl,
        header: {
            'User-Agent': UAMobile,
            'Referer': 'https://play.svip30.tv/',
        }
    });
}

function decryptVideoUrl(encryptedUrl, encodeType, srcNum) {
    try {
        if (!encodeType) encodeType = srcNum === 2 ? 'lzm3u8' : 'uvw';
        
        for (let offset = 1; offset < 50; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64');
                const ascii = decoded.toString('ascii');
                
                const m3u8Pos = ascii.indexOf('.m3u8');
                if (m3u8Pos === -1) continue;
                
                let path = '';
                
                if (encodeType.includes('lzm3u8')) {
                    let startPos = -1;
                    for (let i = m3u8Pos - 1; i >= 0; i--) {
                        const byte = decoded[i];
                        if (byte >= 32 && byte <= 126) {
                            startPos = i;
                        } else {
                            if (startPos !== -1 && startPos < m3u8Pos - 20) break;
                        }
                    }
                    
                    if (startPos !== -1) {
                        path = ascii.substring(startPos, m3u8Pos + 5);
                        path = path.replace(/[^\x20-\x7E]/g, '');
                        
                        if (path.match(/^\/(\d{5})\//)) {
                            path = path.replace(/^\/(\d{5})\//, '/2$1/');
                        }
                    }
                }
                
                if (!path && encodeType.includes('uvw')) {
                    let startPos = -1;
                    for (let i = m3u8Pos - 1; i >= 0; i--) {
                        const byte = decoded[i];
                        if (byte >= 32 && byte <= 126) {
                            startPos = i;
                        } else {
                            if (startPos !== -1 && startPos < m3u8Pos - 30) break;
                        }
                    }
                    
                    if (startPos !== -1) {
                        path = ascii.substring(startPos, m3u8Pos + 5);
                        path = path.replace(/[^\x20-\x7E]/g, '');
                    }
                    
                    if (!path || path.length < 15) {
                        const idMatch = ascii.match(/(\d{5,7}\/\d{5,7})/);
                        if (idMatch) {
                            const basePath = idMatch[1];
                            const epMatch = ascii.match(/(EP\d{2}\.m3u8)/);
                            const numMatch = ascii.match(/(\d{1,2}\.m3u8)/);
                            
                            if (epMatch) {
                                path = '/' + basePath + '/' + epMatch[1];
                            } else if (numMatch) {
                                path = '/' + basePath + '/' + numMatch[1];
                            } else {
                                const simpleMatch = ascii.match(/(\d+\/[\w\/\-]+\.m3u8)/);
                                if (simpleMatch) {
                                    path = '/' + simpleMatch[1];
                                }
                            }
                            if (path) {
                                path = path.replace(/[^\x20-\x7E\/\.]/g, '');
                            }
                        }
                    }
                }
                
                if (!path) {
                    let startPos = -1;
                    for (let i = m3u8Pos - 1; i >= 0; i--) {
                        const byte = decoded[i];
                        if (byte >= 32 && byte <= 126) {
                            startPos = i;
                        } else {
                            if (startPos !== -1 && startPos < m3u8Pos - 20) break;
                        }
                    }
                    
                    if (startPos !== -1) {
                        path = ascii.substring(startPos, m3u8Pos + 5);
                        path = path.replace(/[^\x20-\x7E]/g, '');
                    }
                }
                
                if (path && path.includes('.m3u8')) {
                    if (!path.startsWith('/')) path = '/' + path;
                    
                    if (path.length >= 10) {
                        return 'https://play.svip30.tv' + path;
                    }
                }
                
            } catch (e) {
                continue;
            }
        }
        
        return null;
    } catch (e) {
        return null;
    }
}

async function search(wd, quick) {
    const postData = 'wd=' + encodeURIComponent(wd);
    const html = await request(HOST + '/index.php?m=vod-search', postData);
    const $ = load(html);
    const videos = [];
    
    $('li').each((i, li) => {
        const $li = $(li);
        const $a = $li.find('a[href*="/vod-detail-id-"]');
        if ($a.length > 0) {
            const href = $a.attr('href');
            const id = href.match(/\/vod-detail-id-(\d+)\.html/)?.[1];
            
            if (id) {
                let vodPic = $li.find('img').attr('data-src') || 
                            $li.find('img').attr('data-echo') || 
                            $li.find('img').attr('src') || '';
                
                if (vodPic && !vodPic.startsWith('http')) {
                    if (vodPic.startsWith('//')) {
                        vodPic = 'https:' + vodPic;
                    } else if (vodPic.startsWith('/')) {
                        vodPic = HOST + vodPic;
                    }
                }
                
                const title = $a.attr('title') || $li.find('.sTit').text().trim() || '';
                const remarks = $li.find('.sDes').text().trim() || '';
                
                if (title) {
                    videos.push({
                        vod_id: id,
                        vod_name: title,
                        vod_pic: vodPic,
                        vod_remarks: remarks,
                    });
                }
            }
        }
    });
    
    return JSON.stringify({
        list: videos,
    });
}

export function __jsEvalReturn() {
    return {
        init: init,
        home: home,
        homeVod: homeVod,
        category: category,
        detail: detail,
        play: play,
        search: search,
    };
}
