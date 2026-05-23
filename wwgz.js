import { Crypto, load, _ } from 'assets://js/lib/cat.js';

let key = 'wwgz';
let HOST = 'https://vip.wwgz.cn:5200';
let parseMap = {};
let siteKey = '';
let siteType = 0;

const UAMobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1';

async function request(reqUrl) {
    let res = await req(reqUrl, {
        method: 'get',
        headers: {
            'User-Agent': UAMobile,
        },
    });
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
        '1':[
            {'key':'class','name':'类型','value':[{'n':'全部','v':'0'},{'n':'动作片','v':'6'},{'n':'喜剧片','v':'7'},{'n':'爱情片','v':'8'},{'n':'科幻片','v':'9'},{'n':'恐怖片','v':'10'},{'n':'剧情片','v':'11'},{'n':'战争片','v':'12'},{'n':'犯罪片','v':'13'},{'n':'悬疑片','v':'14'},{'n':'惊悚片','v':'15'},{'n':'冒险片','v':'16'},{'n':'奇幻片','v':'17'},{'n':'灾难片','v':'18'},{'n':'动画片','v':'19'},{'n':'纪录片','v':'20'}]},
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'美国','v':'美国'},{'n':'韩国','v':'韩国'},{'n':'日本','v':'日本'},{'n':'英国','v':'英国'},{'n':'泰国','v':'泰国'},{'n':'其他','v':'其他'}]},
            {'key':'year','name':'年代','value':[{'n':'全部','v':'0'},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'},{'n':'2019','v':'2019'},{'n':'2018','v':'2018'},{'n':'2017','v':'2017'},{'n':'2016','v':'2016'},{'n':'2015','v':'2015'},{'n':'2014','v':'2014'},{'n':'2013','v':'2013'},{'n':'2012','v':'2012'},{'n':'2011','v':'2011'},{'n':'2010','v':'2010'},{'n':'更早','v':'1900'}]},
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
        ],
        '2':[
            {'key':'class','name':'类型','value':[{'n':'全部','v':'0'},{'n':'国产剧','v':'21'},{'n':'港台剧','v':'22'},{'n':'日韩剧','v':'23'},{'n':'欧美剧','v':'24'},{'n':'其他剧','v':'25'}]},
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'美国','v':'美国'},{'n':'韩国','v':'韩国'},{'n':'日本','v':'日本'},{'n':'英国','v':'英国'},{'n':'泰国','v':'泰国'},{'n':'其他','v':'其他'}]},
            {'key':'year','name':'年代','value':[{'n':'全部','v':'0'},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'},{'n':'2019','v':'2019'},{'n':'2018','v':'2018'}]},
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
        ],
        '3':[
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'美国','v':'美国'},{'n':'韩国','v':'韩国'},{'n':'日本','v':'日本'}]},
            {'key':'year','name':'年代','value':[{'n':'全部','v':'0'},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'}]},
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
        ],
        '4':[
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'日本','v':'日本'},{'n':'美国','v':'美国'}]},
            {'key':'year','name':'年代','value':[{'n':'全部','v':'0'},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'}]},
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
        ],
        '26':[
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
        ],
        '20':[
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
        ],
        '31':[
            {'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}
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
    
    $('section.mod').each((idx, mod) => {
        const $mod = $(mod);
        const $items = $mod.find('li a[href*="/vod-detail-id-"]');
        $items.each((i, item) => {
            const $item = $(item);
            const $img = $item.find('img');
            const href = $item.attr('href');
            const id = href.match(/\/vod-detail-id-(\d+)\.html/)?.[1];
            if (id && videos.filter(v => v.vod_id === id).length === 0) {
                let vodPic = $img.attr('data-echo') || $img.attr('src') || '';
                if (vodPic && !vodPic.startsWith('http')) {
                    vodPic = HOST + vodPic;
                }
                videos.push({
                    vod_id: id,
                    vod_name: $item.attr('title') || $img.attr('alt') || '',
                    vod_pic: vodPic,
                    vod_remarks: $item.find('span.sDes').text().trim() || '',
                });
            }
        });
    });
    
    return JSON.stringify({
        list: videos.slice(0, 40),
    });
}

async function category(tid, pg, filter, extend) {
    if (pg <= 0) pg = 1;
    const classId = extend.class || '0';
    const area = extend.area || '';
    const year = extend.year || '0';
    const letter = extend.letter || '';
    const by = extend.by || 'time';
    
    const link = HOST + '/index.php?m=vod-list-id-' + tid + '-pg-' + pg + '-order--by-' + by + '-class-' + classId + '-year-' + year + '-letter-' + letter + '-area-' + encodeURIComponent(area) + '-lang-.html';
    
    const html = await request(link);
    const $ = load(html);
    const items = $('li a[href*="/vod-detail-id-"]');
    const videos = _.map(items, (item) => {
        const $item = $(item);
        const href = $item.attr('href');
        const id = href.match(/\/vod-detail-id-(\d+)\.html/)?.[1];
        const $img = $item.find('img');
        let vodPic = $img.attr('data-echo') || $img.attr('src') || '';
        if (vodPic && !vodPic.startsWith('http')) {
            vodPic = HOST + vodPic;
        }
        return {
            vod_id: id || '',
            vod_name: $item.attr('title') || $img.attr('alt') || '',
            vod_pic: vodPic,
            vod_remarks: $item.find('span.sDes').text().trim() || '',
        };
    });
    
    const totalText = $('div.page').text().match(/共(\d+)条数据/)?.[1] || '0';
    const total = parseInt(totalText);
    const limit = 30;
    const pageCount = Math.ceil(total / limit) || 1;
    
    return JSON.stringify({
        page: parseInt(pg),
        pagecount: pageCount,
        limit: limit,
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
        vodPic = HOST + vodPic;
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
    const html = await request(HOST + id);
    const $ = load(html);
    
    // 从页面中提取mac_url变量
    let macUrl = '';
    let macFrom = '';
    const $scripts = $('script');
    
    $scripts.each((i, script) => {
        const text = $(script).html() || '';
        if (text.includes("mac_url=")) {
            // 匹配 mac_url='...' 或 mac_url="..."
            const match = text.match(/mac_url\s*=\s*['"]([^'"]+)['"]/);
            if (match) {
                macUrl = match[1];
            }
        }
        if (text.includes("mac_from=")) {
            const match = text.match(/mac_from\s*=\s*['"]([^'"]+)['"]/);
            if (match) {
                macFrom = match[1];
            }
        }
    });
    
    // 如果macUrl以$开头，需要分割
    let videoUrl = macUrl;
    if (macUrl.includes('$')) {
        const parts = macUrl.split('$');
        videoUrl = parts[1] || parts[0]; // 取$后面的部分
    }
    
    // 返回iframe播放器URL，让TVBox加载外部播放器
    const playerUrl = 'https://api.nmvod.me:520/player/?url=' + encodeURIComponent(videoUrl);
    
    return JSON.stringify({
        parse: 1,
        url: playerUrl,
        header: {
            'User-Agent': UAMobile,
        }
    });
}

async function search(wd, quick) {
    const link = HOST + '/index.php?m=vod-search-wd-' + encodeURIComponent(wd) + '.html';
    const html = await request(link);
    const $ = load(html);
    
    const items = $('li a[href*="/vod-detail-id-"]');
    const videos = _.map(items, (item) => {
        const $item = $(item);
        const href = $item.attr('href');
        const id = href.match(/\/vod-detail-id-(\d+)\.html/)?.[1];
        const $img = $item.find('img');
        let vodPic = $img.attr('data-echo') || $img.attr('src') || '';
        if (vodPic && !vodPic.startsWith('http')) {
            vodPic = HOST + vodPic;
        }
        return {
            vod_id: id || '',
            vod_name: $item.attr('title') || $img.attr('alt') || '',
            vod_pic: vodPic,
            vod_remarks: $item.find('span.sDes').text().trim() || '',
        };
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
