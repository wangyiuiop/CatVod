
// 详细分析搜索结果的HTML结构
const fs = require('fs');

try {
    const html = fs.readFileSync('/workspace/yulinling_search.html', 'utf-8');
    console.log('HTML长度:', html.length, '字符\n');
    
    // 查找 data_list 的位置
    const dataListIndex = html.indexOf('id="data_list"');
    if (dataListIndex !== -1) {
        console.log('找到 data_list 在位置:', dataListIndex);
        
        // 提取 data_list 区域的内容
        const startIndex = html.lastIndexOf('<ul', dataListIndex);
        const endIndex = html.indexOf('</ul>', dataListIndex) + 5;
        const ulContent = html.substring(startIndex, endIndex);
        
        console.log('\n=== data_list ul 内容 ===\n');
        console.log(ulContent);
        
        // 查找所有的 li 标签
        const liRegex = /<li[^>]*>([\s\S]*?)<\/li>/g;
        let liMatch;
        let liIndex = 0;
        console.log('\n=== 解析 li 元素 ===\n');
        
        while ((liMatch = liRegex.exec(ulContent)) !== null) {
            liIndex++;
            console.log(`\n--- 第 ${liIndex} 个 li ---\n`);
            console.log(liMatch[1]);
            
            // 查找这个 li 中的链接
            const aRegex = /<a[^>]*href="([^"]*)"[^>]*>/g;
            let aMatch;
            let aIndex = 0;
            while ((aMatch = aRegex.exec(liMatch[1])) !== null) {
                aIndex++;
                console.log(`\n  -- 链接 ${aIndex}: ${aMatch[1]}`);
                
                // 查找 vod-detail-id
                if (aMatch[1].indexOf('vod-detail-id') !== -1) {
                    const idMatch = aMatch[1].match(/vod-detail-id-(\d+)/);
                    if (idMatch) {
                        console.log(`  ✓ 找到视频ID: ${idMatch[1]}`);
                    }
                }
                
                // 查找 title 属性
                const titleMatch = aMatch[0].match(/title="([^"]*)"/);
                if (titleMatch) {
                    console.log(`  标题: ${titleMatch[1]}`);
                }
            }
            
            // 查找图片
            const imgRegex = /<img[^>]*>/g;
            let imgMatch;
            let imgIndex = 0;
            while ((imgMatch = imgRegex.exec(liMatch[1])) !== null) {
                imgIndex++;
                console.log(`\n  -- 图片 ${imgIndex} --`);
                const dataSrc = imgMatch[0].match(/data-src="([^"]*)"/);
                const src = imgMatch[0].match(/src="([^"]*)"/);
                if (dataSrc) console.log(`    data-src: ${dataSrc[1]}`);
                if (src) console.log(`    src: ${src[1]}`);
            }
            
            // 查找 .sTit
            const sTitRegex = /<span[^>]*class="[^"]*sTit[^"]*"[^>]*>([^<]*)<\/span>/;
            const sTitMatch = liMatch[1].match(sTitRegex);
            if (sTitMatch) {
                console.log(`\n  .sTit 标题: ${sTitMatch[1]}`);
            }
        }
    } else {
        console.log('没有找到 data_list');
        // 查找所有包含 vod-detail-id 的链接
        const vodLinkRegex = /<a[^>]*href="([^"]*vod-detail-id-[^"]*)"[^>]*>/g;
        let vodLinkMatch;
        console.log('\n查找所有 vod-detail-id 链接：');
        while ((vodLinkMatch = vodLinkRegex.exec(html)) !== null) {
            console.log(vodLinkMatch[1]);
        }
    }
    
} catch (e) {
    console.error('错误:', e);
}
