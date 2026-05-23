
// 测试正则表达式解析
const fs = require('fs');

function fixUrl(url) {
    if (!url) return '';
    if (url.startsWith('//')) {
        return 'https:' + url;
    }
    return url;
}

// 模拟搜索函数中的正则解析
function parseSearch(html) {
    const list = [];
    
    // 使用正则表达式直接解析HTML
    const dataListMatch = html.match(/<ul[^>]*id="data_list"[^>]*>([\s\S]*?)<\/ul>/);
    if (dataListMatch) {
        console.log('✅ 找到了 data_list');
        const ulContent = dataListMatch[1];
        console.log('ul内容长度:', ulContent.length);
        
        // 匹配每个 li 元素
        const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/g;
        let liMatch;
        let liCount = 0;
        
        while ((liMatch = liRegex.exec(ulContent)) !== null) {
            liCount++;
            const liContent = liMatch[1];
            
            // 提取视频ID
            const hrefMatch = liContent.match(/<a[^>]*href="([^"]*vod-detail-id-(\d+)[^"]*)"[^>]*>/);
            if (!hrefMatch || !hrefMatch[2]) {
                console.log(`❌ 第${liCount}个li没有找到vod-detail-id`);
                continue;
            }
            
            const vodId = hrefMatch[2];
            console.log(`✅ 第${liCount}个li - 视频ID: ${vodId}`);
            
            // 提取图片
            let vodPic = '';
            const imgMatch = liContent.match(/<img[^>]*>/);
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
            console.log(`   图片: ${vodPic}`);
            
            // 提取标题
            let vodName = '';
            const sTitMatch = liContent.match(/<span[^>]*class="[^"]*sTit[^"]*"[^>]*>([^<]*)<\/span>/);
            if (sTitMatch) {
                vodName = sTitMatch[1].trim();
            }
            console.log(`   标题: ${vodName}`);
            
            // 提取备注
            let vodRemarks = '';
            const sDesMatch = liContent.match(/<span[^>]*class="[^"]*sDes[^"]*"[^>]*>([\s\S]*?)<\/span>/);
            if (sDesMatch) {
                vodRemarks = sDesMatch[1].trim().replace(/<[^>]*>/g, '');
            }
            
            list.push({
                vod_id: vodId,
                vod_name: vodName,
                vod_pic: vodPic,
                vod_remarks: vodRemarks
            });
        }
    } else {
        console.log('❌ 没有找到 data_list');
    }
    
    return list;
}

// 测试
try {
    const html = fs.readFileSync('/workspace/yulinling_search.html', 'utf-8');
    const results = parseSearch(html);
    
    console.log('\n=== 最终结果 ===');
    console.log('解析到', results.length, '个视频');
    console.log(JSON.stringify(results, null, 2));
} catch (e) {
    console.error('测试出错:', e);
}
