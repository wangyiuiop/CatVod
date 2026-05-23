import { Crypto, load, _ } from 'assets://js/lib/cat.js';

let key = 'ylys';
let HOST = 'https://www.ylys.tv';
let parseMap = {};
let siteKey = '';
let siteType = 0;
let cookkie = '';

const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1';
const UAIPAD = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15 Edg/123.0.0.0';
const UAfirefox = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0';

async function request(reqUrl) {
    let res = await req(reqUrl, {
        method: 'get',
        headers: {
            'User-Agent': UAfirefox,
        },
    });
    return res.content;
}

async function init(cfg) {
    siteKey = cfg.skey;
    siteType = cfg.stype;
    await initParseMap();
}

async function initParseMap() {
    const date = new Date();
    const t = '' + date.getFullYear() + (date.getMonth() + 1) + date.getDate();
    try {
        const js = await request(HOST + '/static/js/playerconfig.js?t=' + t);
        const jsEval = js + '\nMacPlayerConfig';
        const playerList = eval(jsEval).player_list;
        const players = _.values(playerList);
        _.each(players, (item) => {
            if (!item.ps || item.ps == '0') return;
            if (_.isEmpty(item.parse)) return;
            parseMap[item.show] = item.parse;
        });
    } catch(e) {
    }
}

async function home(filter) {
    const classes = [
        {'type_id':'1','type_name':'电影'},
        {'type_id':'2','type_name':'电视剧'},
        {'type_id':'3','type_name':'综艺'},
        {'type_id':'4','type_name':'动漫'}
    ];
    const filterObj = {
        '1':[
            {'key':'cateId','name':'类型','init':'','value':[{'n':'全部','v':'1'},{'n':'动作片','v':'6'},{'n':'喜剧片','v':'7'},{'n':'爱情片','v':'8'},{'n':'科幻片','v':'9'},{'n':'奇幻片','v':'10'},{'n':'恐怖片','v':'11'},{'n':'剧情片','v':'12'},{'n':'战争片','v':'20'},{'n':'纪录片','v':'21'},{'n':'动画片','v':'22'},{'n':'悬疑片','v':'23'},{'n':'冒险片','v':'24'},{'n':'犯罪片','v':'25'},{'n':'惊悚片','v':'26'},{'n':'歌舞片','v':'27'},{'n':'灾难片','v':'28'},{'n':'网络片','v':'29'}]},
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'日本','v':'日本'},{'n':'韩国','v':'韩国'},{'n':'欧美','v':'欧美'},{'n':'英国','v':'英国'},{'n':'泰国','v':'泰国'},{'n':'其它','v':'其它'}]},
            {'key':'lang','name':'语言','value':[{'n':'全部','v':''},{'n':'国语','v':'国语'},{'n':'英语','v':'英语'},{'n':'粤语','v':'粤语'},{'n':'韩语','v':'韩语'},{'n':'日语','v':'日语'},{'n':'西班牙','v':'西班牙'},{'n':'法语','v':'法语'},{'n':'德语','v':'德语'},{'n':'意大利语','v':'意大利语'},{'n':'泰语','v':'泰语'},{'n':'其它','v':'其它'}]},
            {'key':'year','name':'年代','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'},{'n':'2019','v':'2019'},{'n':'2018','v':'2018'},{'n':'2017','v':'2017'},{'n':'2016','v':'2016'},{'n':'2015','v':'2015'},{'n':'2014','v':'2014'},{'n':'2013','v':'2013'},{'n':'2012','v':'2012'},{'n':'2011','v':'2011'},{'n':'更早','v':'更早'}]},
            {'key':'letter','name':'字母','value':[{'n':'全部','v':''},{'n':'A','v':'A'},{'n':'B','v':'B'},{'n':'C','v':'C'},{'n':'D','v':'D'},{'n':'E','v':'E'},{'n':'F','v':'F'},{'n':'G','v':'G'},{'n':'H','v':'H'},{'n':'I','v':'I'},{'n':'J','v':'J'},{'n':'K','v':'K'},{'n':'L','v':'L'},{'n':'M','v':'M'},{'n':'N','v':'N'},{'n':'O','v':'O'},{'n':'P','v':'P'},{'n':'Q','v':'Q'},{'n':'R','v':'R'},{'n':'S','v':'S'},{'n':'T','v':'T'},{'n':'U','v':'U'},{'n':'V','v':'V'},{'n':'W','v':'W'},{'n':'X','v':'X'},{'n':'Y','v':'Y'},{'n':'Z','v':'Z'},{'n':'0-9','v':'0-9'}]},
            {'key':'by','name':'排序','init':'','value':[{'n':'添加时间','v':'time_add'},{'n':'更新时间','v':'time_update'},{'n':'人气排序','v':'hits'},{'n':'评分排序','v':'score'}]}
        ],
        '2':[
            {'key':'cateId','name':'类型','init':'','value':[{'n':'全部','v':'2'},{'n':'国产剧','v':'13'},{'n':'港台泰','v':'14'},{'n':'日剧','v':'15'},{'n':'欧美剧','v':'16'},{'n':'其他剧','v':'25'}]},
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'日本','v':'日本'},{'n':'韩国','v':'韩国'},{'n':'欧美','v':'欧美'},{'n':'英国','v':'英国'},{'n':'泰国','v':'泰国'},{'n':'其它','v':'其它'}]},
            {'key':'lang','name':'语言','value':[{'n':'全部','v':''},{'n':'国语','v':'国语'},{'n':'英语','v':'英语'},{'n':'粤语','v':'粤语'},{'n':'韩语','v':'韩语'},{'n':'日语','v':'日语'},{'n':'西班牙','v':'西班牙'},{'n':'法语','v':'法语'},{'n':'德语','v':'德语'},{'n':'意大利语','v':'意大利语'},{'n':'泰语','v':'泰语'},{'n':'其它','v':'其它'}]},
            {'key':'year','name':'年代','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'},{'n':'2019','v':'2019'},{'n':'2018','v':'2018'},{'n':'2017','v':'2017'},{'n':'2016','v':'2016'},{'n':'2015','v':'2015'},{'n':'2014','v':'2014'},{'n':'2013','v':'2013'},{'n':'2012','v':'2012'},{'n':'2011','v':'2011'},{'n':'更早','v':'更早'}]},
            {'key':'letter','name':'字母','value':[{'n':'全部','v':''},{'n':'A','v':'A'},{'n':'B','v':'B'},{'n':'C','v':'C'},{'n':'D','v':'D'},{'n':'E','v':'E'},{'n':'F','v':'F'},{'n':'G','v':'G'},{'n':'H','v':'H'},{'n':'I','v':'I'},{'n':'J','v':'J'},{'n':'K','v':'K'},{'n':'L','v':'L'},{'n':'M','v':'M'},{'n':'N','v':'N'},{'n':'O','v':'O'},{'n':'P','v':'P'},{'n':'Q','v':'Q'},{'n':'R','v':'R'},{'n':'S','v':'S'},{'n':'T','v':'T'},{'n':'U','v':'U'},{'n':'V','v':'V'},{'n':'W','v':'W'},{'n':'X','v':'X'},{'n':'Y','v':'Y'},{'n':'Z','v':'Z'},{'n':'0-9','v':'0-9'}]},
            {'key':'by','name':'排序','init':'','value':[{'n':'添加时间','v':'time_add'},{'n':'更新时间','v':'time_update'},{'n':'人气排序','v':'hits'},{'n':'评分排序','v':'score'}]}
        ],
        '3':[
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'日本','v':'日本'},{'n':'韩国','v':'韩国'},{'n':'欧美','v':'欧美'},{'n':'英国','v':'英国'},{'n':'泰国','v':'泰国'},{'n':'其它','v':'其它'}]},
            {'key':'lang','name':'语言','value':[{'n':'全部','v':''},{'n':'国语','v':'国语'},{'n':'英语','v':'英语'},{'n':'粤语','v':'粤语'},{'n':'韩语','v':'韩语'},{'n':'日语','v':'日语'},{'n':'西班牙','v':'西班牙'},{'n':'法语','v':'法语'},{'n':'德语','v':'德语'},{'n':'意大利语','v':'意大利语'},{'n':'泰语','v':'泰语'},{'n':'其它','v':'其它'}]},
            {'key':'year','name':'年代','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'},{'n':'2019','v':'2019'},{'n':'2018','v':'2018'},{'n':'2017','v':'2017'},{'n':'2016','v':'2016'},{'n':'2015','v':'2015'},{'n':'2014','v':'2014'},{'n':'2013','v':'2013'},{'n':'2012','v':'2012'},{'n':'2011','v':'2011'},{'n':'更早','v':'更早'}]},
            {'key':'letter','name':'字母','value':[{'n':'全部','v':''},{'n':'A','v':'A'},{'n':'B','v':'B'},{'n':'C','v':'C'},{'n':'D','v':'D'},{'n':'E','v':'E'},{'n':'F','v':'F'},{'n':'G','v':'G'},{'n':'H','v':'H'},{'n':'I','v':'I'},{'n':'J','v':'J'},{'n':'K','v':'K'},{'n':'L','v':'L'},{'n':'M','v':'M'},{'n':'N','v':'N'},{'n':'O','v':'O'},{'n':'P','v':'P'},{'n':'Q','v':'Q'},{'n':'R','v':'R'},{'n':'S','v':'S'},{'n':'T','v':'T'},{'n':'U','v':'U'},{'n':'V','v':'V'},{'n':'W','v':'W'},{'n':'X','v':'X'},{'n':'Y','v':'Y'},{'n':'Z','v':'Z'},{'n':'0-9','v':'0-9'}]},
            {'key':'by','name':'排序','init':'','value':[{'n':'添加时间','v':'time_add'},{'n':'更新时间','v':'time_update'},{'n':'人气排序','v':'hits'},{'n':'评分排序','v':'score'}]}
        ],
        '4':[
            {'key':'area','name':'地区','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'日本','v':'日本'},{'n':'韩国','v':'韩国'},{'n':'欧美','v':'欧美'},{'n':'英国','v':'英国'},{'n':'泰国','v':'泰国'},{'n':'其它','v':'其它'}]},
            {'key':'lang','name':'语言','value':[{'n':'全部','v':''},{'n':'国语','v':'国语'},{'n':'英语','v':'英语'},{'n':'粤语','v':'粤语'},{'n':'韩语','v':'韩语'},{'n':'日语','v':'日语'},{'n':'西班牙','v':'西班牙'},{'n':'法语','v':'法语'},{'n':'德语','v':'德语'},{'n':'意大利语','v':'意大利语'},{'n':'泰语','v':'泰语'},{'n':'其它','v':'其它'}]},
            {'key':'year','name':'年代','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'},{'n':'2019','v':'2019'},{'n':'2018','v':'2018'},{'n':'2017','v':'2017'},{'n':'2016','v':'2016'},{'n':'2015','v':'2015'},{'n':'2014','v':'2014'},{'n':'2013','v':'2013'},{'n':'2012','v':'2012'},{'n':'2011','v':'2011'},{'n':'更早','v':'更早'}]},
            {'key':'letter','name':'字母','value':[{'n':'全部','v':''},{'n':'A','v':'A'},{'n':'B','v':'B'},{'n':'C','v':'C'},{'n':'D','v':'D'},{'n':'E','v':'E'},{'n':'F','v':'F'},{'n':'G','v':'G'},{'n':'H','v':'H'},{'n':'I','v':'I'},{'n':'J','v':'J'},{'n':'K','v':'K'},{'n':'L','v':'L'},{'n':'M','v':'M'},{'n':'N','v':'N'},{'n':'O','v':'O'},{'n':'P','v':'P'},{'n':'Q','v':'Q'},{'n':'R','v':'R'},{'n':'S','v':'S'},{'n':'T','v':'T'},{'n':'U','v':'U'},{'n':'V','v':'V'},{'n':'W','v':'W'},{'n':'X','v':'X'},{'n':'Y','v':'Y'},{'n':'Z','v':'Z'},{'n':'0-9','v':'0-9'}]},
            {'key':'by','name':'排序','init':'','value':[{'n':'添加时间','v':'time_add'},{'n':'更新时间','v':'time_update'},{'n':'人气排序','v':'hits'},{'n':'评分排序','v':'score'}]}
        ]
    };
    return JSON.stringify({
        class: classes,
        filters: filterObj,
    });
}

async function homeVod() {}

async function category(tid, pg, filter, extend) {
    if (pg <= 0) pg = 1;
    const cateId = extend.cateId || tid;
    const area = extend.area || '';
    const lang = extend.lang || '';
    const year = extend.year || '';
    const letter = extend.letter || '';
    const by = extend.by || '';
    
    // 根据实际浏览器测试，URL是固定长度的连字符分隔格式:
    // 完整结构（共12段）：
    // 0:分类  1:地区  2:排序  3:空  4:语言  5:字母  6:空  7:空  8:分页  9:空  10:空  11:年份
    // 实际测试示例：
    // 第一页默认: /vodshow/1-----------/
    // 第二页默认: /vodshow/1--------2---/
    // 人气排序: /vodshow/1--hits---------/
    // 国语筛选: /vodshow/1----国语-------/
    // 字母A筛选: /vodshow/1----国语-A------/
    // 动作片+大陆+人气排序+2025: /vodshow/6-%E5%A4%A7%E9%99%86-hits---------2025/
    const parts = [
        cateId,  // 0: 分类ID
        area ? encodeURIComponent(area) : '',  // 1: 地区
        by || '',  // 2: 排序
        '',  // 3: 保留
        lang ? encodeURIComponent(lang) : '',  // 4: 语言
        letter || '',  // 5: 字母
        '',  // 6: 保留
        '',  // 7: 保留
        pg > 1 ? pg : '',  // 8: 分页
        '',  // 9: 保留
        '',  //10: 保留
        year || '',  //11: 年份
    ];
    
    const path = parts.join('-') + '/';
    
    const link = HOST + '/vodshow/' + path;
    const html = await request(link);
    const $ = load(html);
    const items = $('a.module-poster-item.module-item');
    const videos = _.map(items, (item) => {
        const $item = $(item);
        const a = $item;
        const img = $item.find('img:first');
        const remarks = $item.find('div.module-item-note').text().trim();
        let vodPic = img.attr('data-original') || img.attr('src');
        if (vodPic && !vodPic.startsWith('http')) {
            vodPic = HOST + vodPic;
        }
        return {
            vod_id: a.attr('href').replace(/.*?\/voddetail\/(.*)\//g, '$1'),
            vod_name: a.attr('title'),
            vod_pic: vodPic,
            vod_remarks: remarks,
        };
    });
    const limit = 12;
    const hasMore = $('div#page > a:contains(下一页)').length > 0;
    const pgCount = hasMore ? parseInt(pg) + 1 : parseInt(pg);
    return JSON.stringify({
        page: parseInt(pg),
        pagecount: pgCount,
        limit: limit,
        total: limit * pgCount,
        list: videos,
    });
}

async function detail(id) {
    const html = await request(HOST + '/voddetail/' + id + '/');
    const $ = load(html);
    let vodPic = $('.module-info-poster img:first').attr('data-original') || $('.module-info-poster img:first').attr('src');
    if (vodPic && !vodPic.startsWith('http')) {
        vodPic = HOST + vodPic;
    }
    const vod = {
        vod_id: id,
        vod_name: $('h1:first').text().trim(),
        vod_type: $('.module-info-tag a:eq(2)').text().trim(),
        vod_year: $('.module-info-tag a:eq(0)').text().trim(),
        vod_area: $('.module-info-tag a:eq(1)').text().trim(),
        vod_actor: $('.module-info-item:contains(主演：)').text().trim().substring(3).replace(/\/$/, ''),
        vod_director: $('.module-info-item:contains(导演：)').text().trim().substring(3).replace(/\/$/, ''),
        vod_pic: vodPic,
        vod_remarks: $('.module-info-item:contains(更新：)').next().text(),
        vod_content: $('.module-info-introduction-content').text().trim(),
    };
    const playMap = {};
    const tabs = $('.module-tab-item.tab-item span');
    const playlists = $('.module-play-list');
    _.each(tabs, (tab, i) => {
        const $tab = $(tab);
        const from = $tab.text().trim();
        let list = playlists[i];
        list = $(list).find('a');
        _.each(list, (it) => {
            const $it = $(it);
            let title = $it.find('span').text();
            const playUrl = $it.attr('href');
            if (_.isEmpty(title)) title = $it.text();
            if (!playMap.hasOwnProperty(from)) {
                playMap[from] = [];
            }
            playMap[from].push(title + '$' + playUrl);
        });
    });
    vod.vod_play_from = _.keys(playMap).join('$$$');
    const urls = _.values(playMap);
    const vod_play_url = _.map(urls, (urlist) => {
        return urlist.join('#');
    });
    vod.vod_play_url = vod_play_url.join('$$$');
    return JSON.stringify({
        list: [vod],
    });
}

async function play(flag, id, flags) {
    const link = HOST + id;
    const html = await request(link);
    const $ = load(html);
    const script = $('script:contains(player_aaaa)').html();
    let playUrl = '';
    if (script) {
        const js = JSON.parse(script.replace('var player_aaaa=', ''));
        playUrl = js.url;
    }
    return JSON.stringify({
        parse: 0,
        url: playUrl,
        header: {
            'User-Agent': UA,
        }
    });
}

async function search(wd, quick) {
    const html = await request(HOST + '/vodsearch/-------------/?wd=' + encodeURIComponent(wd));
    const $ = load(html);
    const items = $('.module-card-item.module-item');
    const videos = _.map(items, (item) => {
        const $item = $(item);
        const a = $item.find('.module-card-item-poster');
        const img = $item.find('img:first');
        const remarks = $item.find('div.module-item-note').text().trim();
        let vodPic = img.attr('data-original') || img.attr('src');
        if (vodPic && !vodPic.startsWith('http')) {
            vodPic = HOST + vodPic;
        }
        return {
            vod_id: a.attr('href').replace(/.*?\/voddetail\/(.*)\//g, '$1'),
            vod_name: img.attr('alt'),
            vod_pic: vodPic,
            vod_remarks: remarks,
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
