import { Crypto, load, _ } from 'assets://js/lib/cat.js';

const HOST = 'https://vip.wwgz.cn:5200';
const UA =
    'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1';

let siteKey = '';
let siteType = '';

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

function parseVodList($, selector) {
    const list = [];

    $(selector).each((_, el) => {
        const $el = $(el);

        // 尝试找到包含 vod-detail-id 的链接
        let $a = $el.find('a[href*="/vod-detail-id-"]');
        
        // 如果直接找不到，就找第一个链接
        if (!$a.length) {
            $a = $el.find('a').first();
        }

        if (!$a.length) return;

        const href = $a.attr('href') || '';

        // 从链接中提取视频ID
        const vodIdMatch = href.match(/vod-detail-id-(\d+)/);
        if (!vodIdMatch) return;
        const vodId = vodIdMatch[1];

        // 获取图片地址
        let vodPic = '';
        const $img = $el.find('img').first();
        if ($img.length) {
            vodPic = $img.attr('data-src') || $img.attr('data-echo') || $img.attr('src') || '';
        }
        vodPic = fixUrl(vodPic);

        // 获取视频名称
        let vodName = $a.attr('title') || '';
        if (!vodName) {
            const $sTit = $el.find('.sTit');
            if ($sTit.length) {
                vodName = $sTit.text().trim();
            }
        }
        if (!vodName) {
            vodName = $el.text().trim().split('\n')[0] || '';
        }

        // 获取备注信息
        let vodRemarks = '';
        const $sDes = $el.find('.sDes');
        if ($sDes.length) {
            vodRemarks = $sDes.text().trim();
        }
        if (!vodRemarks) {
            const $remarks = $el.find('.remarks');
            if ($remarks.length) {
                vodRemarks = $remarks.text().trim();
            }
        }

        list.push({
            vod_id: vodId,
            vod_name: vodName,
            vod_pic: vodPic,
            vod_remarks: vodRemarks,
        });
    });

    return list;
}

function getFilters() {
    const years = [{ n: '全部', v: '0' }];

    for (let i = 2026; i >= 2018; i--) {
        years.push({
            n: String(i),
            v: String(i),
        });
    }

    return {
        '1': [
            {
                key: 'by',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                    { n: '评分', v: 'score' },
                ],
            },
            {
                key: 'area',
                name: '地区',
                value: [
                    { n: '全部', v: '' },
                    { n: '大陆', v: '大陆' },
                    { n: '香港', v: '香港' },
                    { n: '台湾', v: '台湾' },
                    { n: '美国', v: '美国' },
                    { n: '韩国', v: '韩国' },
                    { n: '日本', v: '日本' },
                ],
            },
            {
                key: 'year',
                name: '年代',
                value: years,
            },
        ],
        '2': [
            {
                key: 'by',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                    { n: '评分', v: 'score' },
                ],
            },
            {
                key: 'year',
                name: '年代',
                value: years,
            },
        ],
        '3': [
            {
                key: 'by',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                ],
            },
        ],
        '4': [
            {
                key: 'by',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                ],
            },
        ],
        '26': [
            {
                key: 'by',
                name: '排序',
                value: [
                    { n: '时间', v: 'time' },
                    { n: '人气', v: 'hits' },
                ],
            },
        ],
    };
}

async function init(cfg) {
    siteKey = cfg.skey;
    siteType = cfg.stype;
}

async function home(filter) {
    return JSON.stringify({
        class: [
            { type_id: '1', type_name: '电影' },
            { type_id: '2', type_name: '连续剧' },
            { type_id: '3', type_name: '综艺' },
            { type_id: '4', type_name: '动漫' },
            { type_id: '26', type_name: '短剧' },
        ],
        filters: getFilters(),
    });
}

async function homeVod() {
    const html = await request(HOST);

    const $ = load(html);

    const list = parseVodList($, 'section.mod li');

    return JSON.stringify({
        list: list.slice(0, 40),
    });
}

async function category(tid, pg, filter, extend) {
    pg = pg || 1;

    const by = extend.by || 'time';
    const area = extend.area || '';
    const year = extend.year || '0';

    const url =
        HOST +
        `/index.php?m=vod-list-id-${tid}-pg-${pg}-order--by-${by}-class-0-year-${year}-letter--area-${encodeURIComponent(area)}-lang-.html`;

    const html = await request(url);

    const $ = load(html);

    const list = parseVodList($, 'ul.resize_list li');

    const pageText = $('body').text();

    const total =
        parseInt(pageText.match(/共(\d+)条数据/)?.[1] || '0');

    const pagecount =
        parseInt(pageText.match(/当前:\d+\/(\d+)页/)?.[1] || '1');

    return JSON.stringify({
        page: parseInt(pg),
        pagecount: pagecount,
        limit: 30,
        total: total,
        list,
    });
}

async function detail(id) {
    const html = await request(
        HOST + `/vod-detail-id-${id}.html`
    );

    const $ = load(html);

    const title =
        $('h1.title').text().trim() ||
        $('title').text().trim();

    let vodPic =
        $('section.page-hd img').attr('src') ||
        $('img').first().attr('src') ||
        '';

    vodPic = fixUrl(vodPic);

    const vodContent =
        $('article.detail-con p').text().trim() ||
        $('.content').text().trim() ||
        '';

    let vodActor = '';
    let vodDirector = '';
    let vodYear = '';

    $('.desc_item').each((_, el) => {
        const text = $(el).text();

        if (text.includes('主演')) {
            vodActor = text.replace('主演:', '').trim();
        }

        if (text.includes('导演')) {
            vodDirector = text.replace('导演:', '').trim();
        }

        if (text.includes('年代')) {
            vodYear = text.match(/\d{4}/)?.[0] || '';
        }
    });

    const playMap = {};

    $('.numList').each((i, el) => {
        const from =
            $('.play_source_tab a').eq(i).text().trim() ||
            `线路${i + 1}`;

        playMap[from] = [];

        $(el)
            .find('a')
            .each((_, a) => {
                const name = $(a).text().trim();

                const href = $(a).attr('href') || '';

                playMap[from].push(name + '$' + href);
            });
    });

    const vod = {
        vod_id: id,
        vod_name: title,
        vod_pic: vodPic,
        vod_actor: vodActor,
        vod_director: vodDirector,
        vod_year: vodYear,
        vod_content: vodContent,
        vod_play_from: _.keys(playMap).join('$$$'),
        vod_play_url: _.values(playMap)
            .map((e) => e.join('#'))
            .join('$$$'),
    };

    return JSON.stringify({
        list: [vod],
    });
}

function decodeBase64(str) {
    try {
        return Crypto.enc.Utf8.stringify(
            Crypto.enc.Base64.parse(str)
        );
    } catch (e) {
        return str;
    }
}

async function play(flag, id, flags) {
    const playUrl = HOST + id;

    const html = await request(playUrl);

    let player = html.match(/player_aaaa\s*=\s*(\{.*?\})</);

    if (!player) {
        player = html.match(/r player_aaaa=(\{.*?\})/);
    }

    if (!player) {
        return JSON.stringify({
            parse: 1,
            url: playUrl,
        });
    }

    let data = {};

    try {
        data = JSON.parse(player[1]);
    } catch (e) {}

    let url = data.url || '';

    if (data.encrypt == '1') {
        url = unescape(url);
    } else if (data.encrypt == '2') {
        url = unescape(decodeBase64(url));
    }

    if (
        url.includes('.m3u8') ||
        url.includes('.mp4')
    ) {
        return JSON.stringify({
            parse: 0,
            url,
            header: {
                'User-Agent': UA,
                'Referer': HOST + '/',
            },
        });
    }

    return JSON.stringify({
        parse: 1,
        url,
        header: {
            'User-Agent': UA,
            'Referer': HOST + '/',
        },
    });
}

async function search(wd, quick) {
    const html = await request(
        HOST + '/index.php?m=vod-search',
        'wd=' + encodeURIComponent(wd)
    );

    const $ = load(html);
    
    // 尝试多种选择器来找到视频列表
    let list = parseVodList($, '#data_list li');
    
    // 如果第一种方法没找到结果，尝试其他方式
    if (list.length === 0) {
        // 尝试查找所有包含 vod-detail-id 的链接
        list = [];
        $('a[href*="/vod-detail-id-"]').each((_, a) => {
            const $a = $(a);
            const href = $a.attr('href');
            const vodIdMatch = href.match(/vod-detail-id-(\d+)/);
            if (!vodIdMatch) return;
            
            const vodId = vodIdMatch[1];
            
            // 找到包含这个链接的父级 li 元素
            const $li = $a.closest('li');
            if ($li.length) {
                // 检查这个 ID 是否已经被添加
                const alreadyExists = list.some(item => item.vod_id === vodId);
                if (!alreadyExists) {
                    let vodPic = '';
                    const $img = $li.find('img').first();
                    if ($img.length) {
                        vodPic = $img.attr('data-src') || $img.attr('data-echo') || $img.attr('src') || '';
                        vodPic = fixUrl(vodPic);
                    }
                    
                    let vodName = $a.attr('title') || '';
                    if (!vodName) {
                        const $sTit = $li.find('.sTit');
                        if ($sTit.length) {
                            vodName = $sTit.text().trim();
                        }
                    }
                    
                    list.push({
                        vod_id: vodId,
                        vod_name: vodName,
                        vod_pic: vodPic,
                        vod_remarks: ''
                    });
                }
            }
        });
    }

    return JSON.stringify({
        list,
    });
}

export function __jsEvalReturn() {
    return {
        init,
        home,
        homeVod,
        category,
        detail,
        play,
        search,
    };
}
