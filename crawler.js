const HOST = 'https://vip.wwgz.cn:5200';
const UA = 'Mozilla/5.0 (Linux; Android 13; M2102J2SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/145.0.7632.7 Mobile Safari/537.36';

async function request(url, data = null) {
    const res = await req(url, {
        method: data ? 'post' : 'get',
        headers: {
            'User-Agent': UA,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': HOST + '/',
        },
        data,
    });
    return res.content || '';
}

function fixUrl(url) {
    if (!url) return '';
    if (url.startsWith('//')) {
        return 'https:' + url;
    }
    if (url.startsWith('/')) {
        return HOST + url;
    }
    return url;
}

function getList(html) {
    let videos = [];
    let selector = '';
    if (html.includes('class="globalPicList"')) selector = '.globalPicList&&li';
    else if (html.includes('class="ulPicTxt')) selector = '.ulPicTxt&&li';
    if (!selector) return videos;
    let items = pdfa(html, selector);
    items.forEach(it => {
        let idMatch = it.match(/href="(.*?)"/);
        let nameMatch = it.match(/<span class="sTit">(.*?)<\/span>/);
        let picMatch = it.match(/data-src="(.*?)"/) || it.match(/src="(.*?)"/);
        let remarksMatch = it.match(/<span>([\s\S]*?)<em>/) || it.match(/<span class="sStyle">([\s\S]*?)<\/span>/);
        if (idMatch && nameMatch) {
            let pic = picMatch ? (picMatch[1] || picMatch[2]) : "";
            videos.push({
                vod_id: idMatch[1],
                vod_name: nameMatch?.[1]?.trim() || "未知片名",
                vod_pic: pic.startsWith('/') ? HOST + pic : fixUrl(pic),
                vod_remarks: remarksMatch?.[1]?.trim() || "未提供"
            });
        }
    });
    return videos;
}

async function init(cfg) {
}

async function home(filter) {
    let classes = [
        { "type_id": "1", "type_name": "电影" },
        { "type_id": "2", "type_name": "剧集" },
        { "type_id": "3", "type_name": "综艺" },
        { "type_id": "4", "type_name": "动漫" },
        { "type_id": "26", "type_name": "短剧" }
    ];
    
    let common_areas = ["全部", "大陆", "香港", "台湾", "美国", "韩国", "日本", "泰国", "新加坡", "马来西亚", "印度", "英国", "法国", "加拿大", "西班牙", "俄罗斯", "其它"];
    let common_years = ["全部", "2026", "2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012"];
    
    let area_values = common_areas.map(a => ({ "n": a, "v": a === "全部" ? "" : a }));
    let year_values = common_years.map(y => ({ "n": y, "v": y === "全部" ? "0" : y }));
    let by_values = [
        { "n": "时间", "v": "-by-time" },
        { "n": "人气", "v": "-by-hits" },
        { "n": "评分", "v": "-by-score" }
    ];

    let movie_sub_classes = [
        { "n": "全部类型", "v": "1" },
        { "n": "动作片", "v": "5" },
        { "n": "喜剧片", "v": "6" },
        { "n": "爱情片", "v": "7" },
        { "n": "科幻片", "v": "8" },
        { "n": "恐怖片", "v": "9" },
        { "n": "剧情片", "v": "10" },
        { "n": "战争片", "v": "11" },
        { "n": "惊悚片", "v": "16" },
        { "n": "奇幻片", "v": "17" }
    ];

    let tv_sub_classes = [
        { "n": "全部", "v": "2" },
        { "n": "国产剧", "v": "12" },
        { "n": "港台泰", "v": "13" },
        { "n": "日韩剧", "v": "14" },
        { "n": "欧美剧", "v": "15" }
    ];

    let variety_sub_classes = [
        { "n": "全部", "v": "3" }
    ];

    let anime_sub_classes = [
        { "n": "全部", "v": "4" }
    ];

    let short_sub_classes = [
        { "n": "全部", "v": "26" }
    ];

    let filter_dict = {};
    classes.forEach(c => {
        let f = [];
        let sub_classes = [];
        
        if (c.type_id === "1") {
            sub_classes = movie_sub_classes;
        } else if (c.type_id === "2") {
            sub_classes = tv_sub_classes;
        } else if (c.type_id === "3") {
            sub_classes = variety_sub_classes;
        } else if (c.type_id === "4") {
            sub_classes = anime_sub_classes;
        } else if (c.type_id === "26") {
            sub_classes = short_sub_classes;
        } else {
            sub_classes = [{ "n": "全部", "v": c.type_id }];
        }

        f.push({ "key": "class", "name": "类型", "value": sub_classes });
        f.push({ "key": "area", "name": "地区", "value": area_values });
        f.push({ "key": "year", "name": "年代", "value": year_values });
        f.push({ "key": "by", "name": "排序", "value": by_values });
        
        filter_dict[c.type_id] = f;
    });

    return JSON.stringify({
        "class": classes,
        "filters": filter_dict
    });
}

async function homeVod() {
    const html = await request(HOST);
    return JSON.stringify({
        list: getList(html)
    });
}

async function category(tid, pg, filter, extend) {
    let p = pg || 1;
    
    let targetId = (extend && extend.class) ? extend.class : tid;
    let by = (extend && extend.by) ? extend.by : '-by-time';
    let year = (extend && extend.year) ? extend.year : '0';
    let area = (extend && extend.area) ? encodeURIComponent(extend.area) : '';
    
    let url = `${HOST}/vod-list-id-${targetId}-pg-${p}-order-${by}-class-0-year-${year}-letter--area-${area}-lang-.html`;
    
    const html = await request(url);
    return JSON.stringify({
        list: getList(html),
        page: parseInt(p)
    });
}

async function detail(id) {
    const dUrl = HOST + id;
    const dhtml = await request(dUrl);
    const playPageUrl = pdfh(dhtml, '.page-btn a.greenBtn&&href');
    if (!playPageUrl) {
        return JSON.stringify({
            list: []
        });
    }
    const phtml = await request(HOST + playPageUrl);
    
    let playFrom = phtml.match(/mac_from='([\s\S]*?)'/)?.[1] ?? '';
    let playUrl = phtml.match(/mac_url='([\s\S]*?)'/)?.[1] ?? '';

    let targetPlayUrl = '';
    if (playFrom && playUrl) {
        let froms = playFrom.split('$$$');
        let urls = playUrl.split('$$$');
        
        const linePriority = ['uvw', 'lzm3u8'];
        
        for (let line of linePriority) {
            for (let i = 0; i < froms.length; i++) {
                let currentLine = froms[i].trim();
                if (currentLine === line && urls[i]) {
                    targetPlayUrl = urls[i].trim();
                    break;
                }
            }
            if (targetPlayUrl) break;
        }
        
        if (!targetPlayUrl && urls.length > 0) {
            targetPlayUrl = urls[0].trim();
        }
    }

    return JSON.stringify({
        list: [{
            vod_id: id,
            vod_name: (dhtml.match(/<h1 class="title">[\s\S]*?title="[\s\S]*?">([\s\S]*?)<\/a>/) || ['', ''])[1],
            vod_pic: (dhtml.match(/<img src="([\s\S]*?)"/) || ["", ""])[1],
            vod_year: (dhtml.match(/年代：[\s\S]*?<em>([\s\S]*?)<\/em>/) || ['', ''])[1],
            vod_remarks: (dhtml.match(/red">([\s\S]*?)<\/font>/) || ['', ''])[1],
            vod_actor: Array.from(
                dhtml.match(/主演:([\s\S]*?)<\/div>/)?.[1]?.matchAll(/<a [^>]*>([^<]+)<\/a>/g) || []
            ).map(m => m[1]).join(' / ') || '',
            vod_director: Array.from(
                dhtml.match(/导演:([\s\S]*?)<\/div>/)?.[1]?.matchAll(/<a [^>]*>([^<]+)<\/a>/g) || []
            ).map(m => m[1]).join(' / ') || '',
            vod_content: (dhtml.match(/<p>([\s\S]*?)<\/p>/) || ['', ''])[1].replace(/<.*?>/g, '').replace("简&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;介：", ""),
            vod_play_from: '蓝光',
            vod_play_url: targetPlayUrl
        }]
    });
}

async function search(wd, quick, pg) {
    const html = await request(HOST + '/index.php?m=vod-search', 'wd=' + encodeURIComponent(wd));
    return JSON.stringify({
        list: getList(html)
    });
}

async function play(flag, id, flags) {
    return JSON.stringify({
        parse: 1,
        url: `https://api.nmvod.me:520/player/?url=${id}`,
        header: {
            'User-Agent': UA
        }
    });
}

export function __jsEvalReturn() {
    return {
        init,
        home,
        homeVod,
        category,
        detail,
        search,
        play
    };
}
