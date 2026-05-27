import { Crypto, load, _, jinja2 } from 'assets://js/lib/cat.js';

let key = 'zhuiguang';
let url = 'https://www.4kmovie.top';
let siteKey = '';
let siteType = 0;

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36';

async function request(reqUrl, agentSp, extHeader) {
    let headers = {
        'User-Agent': agentSp || UA,
        'Referer': url,
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'Accept': '*/*'
    };

    if (extHeader) {
        headers = Object.assign(headers, extHeader);
    }

    let res = await req(reqUrl, {
        method: 'get',
        headers: headers,
    });

    return res.content;
}

async function init(cfg) {
    siteKey = cfg.skey;
    siteType = cfg.stype;
}

async function home(filter) {
    let classes = [
        {'type_id': 20, 'type_name': '电影'},
        {'type_id': 37, 'type_name': '电视剧'},
        {'type_id': 45, 'type_name': '综艺'},
        {'type_id': 43, 'type_name': '动漫'},
        {'type_id': 47, 'type_name': 'B站'} 
    ];

    let filterObj = {
        '20':[{'key':'class','name':'剧情','init':'','value':[{'n':'全部','v':''},{'n':'喜剧','v':'喜剧'},{'n':'爱情','v':'爱情'},{'n':'恐怖','v':'恐怖'},{'n':'动作','v':'动作'},{'n':'科幻','v':'科幻'},{'n':'剧情','v':'剧情'},{'n':'战争','v':'战争'},{'n':'警匪','v':'警匪'},{'n':'犯罪','v':'犯罪'},{'n':'动画','v':'动画'},{'n':'奇幻','v':'奇幻'},{'n':'武侠','v':'武侠'},{'n':'冒险','v':'冒险'},{'n':'枪战','v':'枪战'},{'n':'悬疑','v':'悬疑'},{'n':'惊悚','v':'惊悚'},{'n':'经典','v':'经典'},{'n':'青春','v':'青春'},{'n':'文艺','v':'文艺'},{'n':'古装','v':'古装'},{'n':'历史','v':'历史'},{'n':'运动','v':'运动'},{'n':'网络电影','v':'网络电影'}]},{'key':'area','name':'地区','init':'','value':[{'n':'全部','v':''},{'n':'大陆','v':'大陆'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'美国','v':'美国'},{'n':'法国','v':'法国'},{'n':'英国','v':'英国'},{'n':'日本','v':'日本'},{'n':'韩国','v':'韩国'},{'n':'德国','v':'德国'},{'n':'泰国','v':'泰国'},{'n':'印度','v':'印度'},{'n':'意大利','v':'意大利'},{'n':'西班牙','v':'西班牙'},{'n':'加拿大','v':'加拿大'},{'n':'其他','v':'其他'}]},{'key':'lang','name':'语言','init':'','value':[{'n':'全部','v':''},{'n':'国语','v':'国语'},{'n':'英语','v':'英语'},{'n':'粤语','v':'粤语'},{'n':'闽南语','v':'闽南语'},{'n':'韩语','v':'韩语'},{'n':'日语','v':'日语'},{'n':'法语','v':'法语'},{'n':'德语','v':'德语'},{'n':'其它','v':'其它'}]},{'key':'year','name':'年份','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'}]},{'key':'letter','name':'字母','init':'','value':[{'n':'全部','v':''},{'n':'A','v':'A'},{'n':'B','v':'B'},{'n':'C','v':'C'},{'n':'D','v':'D'},{'n':'E','v':'E'},{'n':'F','v':'F'},{'n':'G','v':'G'},{'n':'H','v':'H'},{'n':'I','v':'I'},{'n':'J','v':'J'},{'n':'K','v':'K'},{'n':'L','v':'L'},{'n':'M','v':'M'},{'n':'N','v':'N'},{'n':'O','v':'O'},{'n':'P','v':'P'},{'n':'Q','v':'Q'},{'n':'R','v':'R'},{'n':'S','v':'S'},{'n':'T','v':'T'},{'n':'U','v':'U'},{'n':'V','v':'V'},{'n':'W','v':'W'},{'n':'X','v':'X'},{'n':'Y','v':'Y'},{'n':'Z','v':'Z'},{'n':'0-9','v':'0-9'}]},{'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}],
        '37':[{'key':'class','name':'剧情','init':'','value':[{'n':'全部','v':''},{'n':'古装','v':'古装'},{'n':'战争','v':'战争'},{'n':'青春偶像','v':'青春偶像'},{'n':'喜剧','v':'喜剧'},{'n':'家庭','v':'家庭'},{'n':'犯罪','v':'犯罪'},{'n':'动作','v':'动作'},{'n':'奇幻','v':'奇幻'},{'n':'剧情','v':'剧情'},{'n':'历史','v':'历史'},{'n':'经典','v':'经典'},{'n':'乡村','v':'乡村'},{'n':'情景','v':'情景'},{'n':'商战','v':'商战'},{'n':'网剧','v':'网剧'},{'n':'其他','v':'其他'}]},{'key':'area','name':'地区','init':'','value':[{'n':'全部','v':''},{'n':'内地','v':'内地'},{'n':'韩国','v':'韩国'},{'n':'香港','v':'香港'},{'n':'台湾','v':'台湾'},{'n':'日本','v':'日本'},{'n':'美国','v':'美国'},{'n':'泰国','v':'泰国'},{'n':'印度','v':'印度'},{'n':'英国','v':'英国'},{'n':'新加坡','v':'新加坡'},{'n':'其他','v':'其他'}]},{'key':'lang','name':'语言','init':'','value':[{'n':'全部','v':''},{'n':'国语','v':'国语'},{'n':'英语','v':'英语'},{'n':'粤语','v':'粤语'},{'n':'韩语','v':'韩语'},{'n':'日语','v':'日语'},{'n':'其它','v':'其它'}]},{'key':'year','name':'年份','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'},{'n':'2021','v':'2021'},{'n':'2020','v':'2020'}]},{'key':'letter','name':'字母','init':'','value':[{'n':'全部','v':''},{'n':'A','v':'A'},{'n':'B','v':'B'},{'n':'C','v':'C'},{'n':'D','v':'D'},{'n':'E','v':'E'},{'n':'F','v':'F'},{'n':'G','v':'G'},{'n':'H','v':'H'},{'n':'Z','v':'Z'},{'n':'0-9','v':'0-9'}]},{'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}],
        '45':[{'key':'class','name':'剧情','init':'','value':[{'n':'全部','v':''},{'n':'选秀','v':'选秀'},{'n':'情感','v':'情感'},{'n':'访谈','v':'访谈'},{'n':'播报','v':'播报'},{'n':'旅游','v':'旅游'},{'n':'音乐','v':'音乐'},{'n':'美食','v':'美食'},{'n':'纪实','v':'纪实'},{'n':'游戏互动','v':'游戏互动'},{'n':'财经','v':'财经'},{'n':'求职','v':'求职'}]},{'key':'area','name':'地区','init':'','value':[{'n':'全部','v':''},{'n':'内地','v':'内地'},{'n':'港台','v':'港台'},{'n':'日韩','v':'日韩'},{'n':'欧美','v':'欧美'}]},{'key':'year','name':'年份','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'}]},{'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}],
        '43':[{'key':'class','name':'剧情','init':'','value':[{'n':'全部','v':''},{'n':'情感','v':'情感'},{'n':'科幻','v':'科幻'},{'n':'热血','v':'热血'},{'n':'推理','v':'推理'},{'n':'搞笑','v':'搞笑'},{'n':'冒险','v':'冒险'},{'n':'萝莉','v':'萝莉'},{'n':'校园','v':'校园'},{'n':'动作','v':'动作'},{'n':'机战','v':'机战'},{'n':'运动','v':'运动'},{'n':'战争','v':'战争'},{'n':'原创','v':'原创'},{'n':'其他','v':'其他'}]},{'key':'area','name':'地区','init':'','value':[{'n':'全部','v':''},{'n':'国产','v':'国产'},{'n':'日本','v':'日本'},{'n':'欧美','v':'欧美'},{'n':'其他','v':'其他'}]},{'key':'year','name':'年份','init':'','value':[{'n':'全部','v':''},{'n':'2026','v':'2026'},{'n':'2025','v':'2025'},{'n':'2024','v':'2024'},{'n':'2023','v':'2023'},{'n':'2022','v':'2022'}]},{'key':'by','name':'排序','value':[{'n':'时间','v':'time'},{'n':'人气','v':'hits'},{'n':'评分','v':'score'}]}],
        '47': [ {'key': 'letter', 'name': '字母', 'init': '', 'value': [{'n': '全部', 'v': ''}, {'n': 'A', 'v': 'A'}, {'n': 'B', 'v': 'B'}, {'n': 'C', 'v': 'C'}, {'n': 'D', 'v': 'D'}, {'n': 'E', 'v': 'E'}, {'n': 'F', 'v': 'F'}, {'n': 'G', 'v': 'G'}, {'n': 'H', 'v': 'H'}, {'n': 'I', 'v': 'I'}, {'n': 'J', 'v': 'J'}, {'n': 'K', 'v': 'K'}, {'n': 'L', 'v': 'L'}, {'n': 'M', 'v': 'M'}, {'n': 'N', 'v': 'N'}, {'n': 'O', 'v': 'O'}, {'n': 'P', 'v': 'P'}, {'n': 'Q', 'v': 'Q'}, {'n': 'R', 'v': 'R'}, {'n': 'S', 'v': 'S'}, {'n': 'T', 'v': 'T'}, {'n': 'U', 'v': 'U'}, {'n': 'V', 'v': 'V'}, {'n': 'W', 'v': 'W'}, {'n': 'X', 'v': 'X'}, {'n': 'Y', 'v': 'Y'}, {'n': 'Z', 'v': 'Z'}, {'n': '0-9', 'v': '0-9'}]},
            {'key': 'by', 'name': '排序', 'value': [{'n': '时间', 'v': 'time'}, {'n': '人气', 'v': 'hits'}, {'n': '评分', 'v': 'score'}]}]};

        return JSON.stringify({
        class: classes,
        filters: filterObj
    });
}

async function homeVod() {
    try {
        const html = await request(url);
        const $ = load(html);
        let videos = [];

        $('.module-poster-item').each((_, item) => {
            const a = $(item);
            const href = a.attr('href');
            if (!href) return;

            const vodIdMatch = href.match(/\/vod(play|detail)\/(\d+)/);
            const title = a.attr('title') || a.find('.module-poster-item-title').text().trim();
            const pic = a.find('.module-item-pic img').attr('data-original') || a.find('.module-item-pic img').attr('src');
            const remarks = a.find('.module-item-note').text().trim();

            videos.push({
                vod_id: vodIdMatch ? vodIdMatch[2] : '',
                vod_name: title,
                vod_pic: pic,
                vod_remarks: remarks
            });
        });

        return JSON.stringify({
            list: videos
        });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}

async function category(tid, pg, filter, extend) {
    pg = pg || 1;
    
    let id = extend.class || tid;
    let area = extend.area || '';
    let by = extend.by || '';
    let cls = extend.class || '';
    let lang = extend.lang || '';
    let letter = extend.letter || '';
    let year = extend.year || '';

    let link = `${url}/vodshow/${id}-${area}-${by}-${cls}-${lang}-${letter}---${pg}---${year}.html`;

    const html = await request(link);
    const $ = load(html);

    const items = $('.module-items a.module-poster-item');

    let videos = _.map(items, (item) => {
        const a = $(item);
        const href = a.attr('href');
        if (!href) return null;

        const vodIdMatch = href.match(/\/vod(play|detail)\/(\d+)/);
        const title = a.attr('title') || a.find('.module-poster-item-title').text().trim();
        const pic = a.find('.module-item-pic img').attr('data-original') || a.find('.module-item-pic img').attr('src');
        const remarks = a.find('.module-item-note').text().trim();

        return {
            vod_id: vodIdMatch ? vodIdMatch[2] : '',
            vod_name: title,
            vod_pic: pic,
            vod_remarks: remarks
        };
    });

    videos = _.filter(videos, (v) => v);
    const hasMore = $('.page-next').length > 0;

    return JSON.stringify({
        page: parseInt(pg),
        pagecount: hasMore ? parseInt(pg) + 1 : parseInt(pg),
        limit: videos.length,
        total: videos.length * (hasMore ? parseInt(pg) + 1 : parseInt(pg)),
        list: videos
    });
}

async function detail(id) {
    const html = await request(`${url}/voddetail/${id}.html`);
    const $ = load(html);

    let vod = {
        vod_id: id,
        vod_name: $('.module-info-heading h1').text().trim() || $('.module-info-heading h1 a').text().trim(),
        vod_pic: $('.module-item-pic img').attr('data-original') || $('.module-item-pic img').attr('src') || '',
        vod_remarks: $('.module-item-note').first().text().trim(),
        vod_content: $('.module-info-item-content').last().text().trim()
    };

    let playMap = {};
    const tabs = $('.module-tab-items .module-tab-item');
    const lists = $('.module-play-list-content');

    _.each(tabs, (tab, i) => {
        let $tab = $(tab).clone();
        $tab.find('small').remove(); 
        let from = $tab.text().trim();

        if (!from) {
            from = '线路' + (i + 1);
        }

        let list = lists[i];
        if (!list) return;

        const aList = $(list).find('a.module-play-list-link');

        _.each(aList, (it) => {
            const title = $(it).find('span').text().trim() || $(it).text().trim();
            const playId = it.attribs.href;

            if (!playMap[from]) {
                playMap[from] = [];
            }
            playMap[from].push(title + '$' + playId);
        });
    });

    vod.vod_play_from = _.keys(playMap).join('$$$');
    vod.vod_play_url = _.map(_.values(playMap), (arr) => arr.join('#')).join('$$$');

    return JSON.stringify({
        list: [vod]
    });
}

async function play(flag, id, flags) {
    try {
        const playLink = id.startsWith('http') ? id : url + id;
        const html = await request(playLink);

        const match = html.match(/var player_aaaa\s*=\s*(\{.*?\})</);
        let playUrl = '';

        if (match) {
            try {
                const player = JSON.parse(match[1]);
                playUrl = player.url || '';
            } catch (e) {}
        }

        if (!playUrl) {
            return JSON.stringify({ parse: 1, jx: 1, url: playLink });
        }

        playUrl = playUrl.replace(/\\\//g, '/').replace(/\\\\/g, '\\');

        if (playUrl.includes('.m3u8') || playUrl.includes('.mp4')) {
            return JSON.stringify({
                parse: 0,
                jx: 0,
                url: playUrl,
                header: {
                    Referer: url,
                    'User-Agent': UA
                }
            });
        }

        try {
            const svipUrl = 'https://svip.qlplayer.cyou/?url=' + encodeURIComponent(playUrl);
            const svipHtml = await request(svipUrl, UA, {
                'Referer': url
            });

            const tokenMatch = svipHtml.match(/apiToken:\s*"([^"]+)"/);

            if (tokenMatch) {
                const token = tokenMatch[1];
                const apiUrl = 'https://svip.qlplayer.cyou/api/resolve.php?token=' + encodeURIComponent(token);

                const apiResStr = await request(apiUrl, UA, {
                    'Referer': 'https://svip.qlplayer.cyou/',
                    'Origin': 'https://svip.qlplayer.cyou',
                    'Accept': 'application/json, text/plain, */*'
                });

                const data = JSON.parse(apiResStr || '{}');

                if (data.code === 200 && data.url) {
                    return JSON.stringify({
                        parse: 0,
                        jx: 0,
                        url: data.url,
                        header: {
                            Referer: 'https://svip.qlplayer.cyou/',
                            'User-Agent': UA
                        }
                    });
                }
            }
        } catch (e) {}

        return JSON.stringify({ parse: 1, jx: 1, url: playUrl });
    } catch (e) {
        return JSON.stringify({ parse: 1, jx: 1, url: id });
    }
}

async function search(wd, quick, pg) {
    try {
        pg = pg || 1;
        const link = `${url}/vodsearch/----------${pg}---.html?wd=${encodeURIComponent(wd)}`;
        const html = await request(link);
        const $ = load(html);
        
        let videos = [];
        let seenIds = new Set();

        const items = $('.module-items .module-item, .module-card-item, .module-poster-item');

        items.each((_, item) => {
            const $item = $(item);
            
            // 提取 vodId：优先从 vodplay，其次从 voddetail
            let vodId = '';
            const allLinks = $item.find('a');
            allLinks.each((_, linkEl) => {
                if (vodId) return;
                const href = $(linkEl).attr('href') || '';
                const playMatch = href.match(/\/vodplay\/(\d+)/);
                const detailMatch = href.match(/\/voddetail\/(\d+)/);
                if (playMatch) vodId = playMatch[1];
                else if (detailMatch) vodId = detailMatch[1];
            });
            
            if (!vodId) return;
            if (seenIds.has(vodId)) return;
            seenIds.add(vodId);
            
            // 尝试多种方式提取标题
            let title = '';
            // 方法1：查找包含 vodplay 的链接
            const playLink = $item.find('a[href*="/vodplay/"]').first();
            if (playLink && playLink.length > 0) {
                title = playLink.attr('title') || playLink.text().trim();
            }
            // 方法2：查找包含 strong 或 b 标签的元素
            if (!title) {
                const strong = $item.find('strong, b').first();
                if (strong && strong.length > 0) {
                    title = strong.text().trim();
                }
            }
            // 方法3：查找任何标题类元素
            if (!title) {
                const titleEl = $item.find('[class*="title"], h1, h2, h3, h4, h5, h6').first();
                if (titleEl && titleEl.length > 0) {
                    title = titleEl.text().trim();
                }
            }
            // 方法4：查找 img 的 alt 属性
            if (!title) {
                const img = $item.find('img').first();
                if (img && img.length > 0) {
                    title = img.attr('alt') || '';
                }
            }
            // 方法5：直接取第一个链接的文本
            if (!title) {
                const firstLink = $item.find('a').first();
                if (firstLink && firstLink.length > 0) {
                    title = firstLink.text().trim();
                }
            }
            
            // 清理标题
            title = title.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
            
            // 提取图片
            let pic = '';
            const img = $item.find('img').first();
            if (img && img.length > 0) {
                pic = img.attr('data-original') || img.attr('data-src') || img.attr('src') || '';
            }
            // 清理图片URL：移除反引号
            pic = pic.replace(/`/g, '').trim();
            
            // 提取备注：尝试多种方式
            let remarks = '';
            // 方法1：查找 module-item-note
            remarks = $item.find('.module-item-note').text().trim();
            // 方法2：查找第一个包含年份或集数的链接
            if (!remarks) {
                $item.find('a').each((_, el) => {
                    if (remarks) return;
                    const text = $(el).text().trim();
                    if (text.includes('集') || text.includes('HD') || text.includes('完结') || text.match(/更新/)) {
                        remarks = text;
                    }
                });
            }
            // 方法3：查找任何备注类元素
            if (!remarks) {
                const noteEl = $item.find('[class*="note"], [class*="serial"], [class*="remark"]').first();
                if (noteEl && noteEl.length > 0) {
                    remarks = noteEl.text().trim();
                }
            }
            // 方法4：查找包含年份信息的文本
            if (!remarks) {
                const yearText = $item.text();
                const yearMatch = yearText.match(/(\d{4}\/[^\/\n]+)/);
                if (yearMatch) {
                    remarks = yearMatch[1];
                }
            }
            
            videos.push({
                vod_id: vodId,
                vod_name: title,
                vod_pic: pic,
                vod_remarks: remarks
            });
        });

        // 清理所有视频数据中的反引号
        videos = videos.map(v => ({
            ...v,
            vod_pic: v.vod_pic.replace(/`/g, '').trim()
        }));

        const hasMore = $('.page-next').length > 0 || $('a:contains("下一页")').length > 0;

        return JSON.stringify({
            page: parseInt(pg),
            pagecount: hasMore ? parseInt(pg) + 1 : parseInt(pg),
            limit: videos.length,
            total: videos.length * (hasMore ? parseInt(pg) + 1 : parseInt(pg)),
            list: videos
        });
    } catch (e) {
        return JSON.stringify({ list: [] });
    }
}
export function __jsEvalReturn() {
    return {
        init,
        home,
        homeVod,
        category,
        detail,
        play,
        search
    };
}
