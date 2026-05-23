
// 测试分析 URL 编码的视频地址问题

const testEncryptedUrl = "这里需要实际的加密字符串"; // 用户提供的 URL 是 https%3A%2F%2Fvip.123pan.cn%2F1853039965%2F202510%2F%25E9%259B%25A8%25E9%259C%2596%25E9%2593%2583%2F%25E9%259B%25A8%25E9%259C%2596%25E9%2593%2583EP01.m3u84

// 首先，让我们分析用户提供的 URL 是编码过的，说明解密后可能已经是 URL 编码的内容
// 让我们先写一个完整的调试函数

function analyzeEncrypted(encryptedUrl) {
    console.log('=== 开始分析加密字符串 ===');
    console.log('原始加密字符串:', encryptedUrl);
    
    for (let offset = 1; offset < 30; offset++) {
        try {
            const testStr = encryptedUrl.substring(offset);
            console.log(`\n尝试偏移 ${offset}:`);
            
            const decoded = Buffer.from(testStr, 'base64');
            console.log('Base64 解码后字节长度:', decoded.length);
            console.log('前100个字节:', Array.from(decoded.subarray(0, 100)).map(b => b.toString(16).padStart(2, '0')).join(' '));
            
            const str = decoded.toString('utf8');
            console.log('解码为字符串（前200字符）:', str.substring(0, 200));
            
            // 检查是否有 URL 编码的内容
            if (str.includes('http%3A') || str.includes('https%3A')) {
                console.log('发现 URL 编码的内容！');
                const decodedUrl = decodeURIComponent(str);
                console.log('解码 URL 编码后:', decodedUrl.substring(0, 300));
            }
            
            // 检查是否有 https:// 直接在里面
            if (str.includes('https://') || str.includes('http://')) {
                console.log('发现完整 URL！');
            }
            
        } catch (e) {
            // 忽略错误
        }
    }
}

console.log('测试函数已创建，请输入实际的加密字符串进行测试');
