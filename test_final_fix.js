// 测试最新修改的解密函数
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64');
                
                // 找到有效路径开始的位置
                let startPos = -1;
                for (let i = 0; i < decoded.length; i++) {
                    // 检查这个位置开始的20个字符中，大部分是否是有效的路径字符
                    let validCount = 0;
                    for (let j = 0; j < Math.min(30, decoded.length - i); j++) {
                        const c = decoded[i + j];
                        if ((c >= 48 && c <= 57) ||   // 数字
                            (c >= 97 && c <= 122) ||   // 小写字母
                            (c >= 65 && c <= 90) ||    // 大写字母
                            c === 47 ||                // /
                            c === 95 ||                // _
                            c === 46) {                // .
                            validCount++;
                        }
                    }
                    
                    // 如果有20个以上有效字符，开始检查是否包含 / 和 .m3u8
                    if (validCount >= 20) {
                        const tempStr = decoded.toString('utf8', i);
                        if (tempStr.includes('.m3u8') && tempStr.includes('/')) {
                            startPos = i;
                            break;
                        }
                    }
                }
                
                if (startPos !== -1) {
                    // 从startPos开始，提取到.m3u8+5的位置
                    const tempStr = decoded.toString('utf8', startPos);
                    const m3u8Pos = tempStr.indexOf('.m3u8');
                    if (m3u8Pos !== -1) {
                        const cleanPath = tempStr.substring(0, m3u8Pos + 5);
                        return 'https://play.svip30.tv/' + cleanPath;
                    }
                }
            } catch (e) {
                // 忽略错误继续尝试
            }
        }
        return null;
    } catch (e) {
        return null;
    }
}

// 测试综艺URL
var varietyUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhbdH0o8t2Y42JR3u4M7T8IZu0Y82D9etSL0zIwMjMwMzIxLzYzOTNfMWU3MWM0MzEvaW5kZXgubTN1OAO0O0OO0O0O';
console.log('测试综艺URL...');
var result1 = decryptVideoUrl(varietyUrl);
console.log(result1);
console.log();

// 测试电影URL
var movieUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhMdT0I8z2c4GJF3u4L7m8NZu0Y82D9e4tSL0zIwMjUwMzI1L2R5LzU0MzBfY2U1ZmJhZjgvWcOF5Lqn5bmg5pa55a6X5ZGY5LmL5Lia54K5Lm0zdTgO0O0O';
console.log('测试电影URL...');
var result2 = decryptVideoUrl(movieUrl);
console.log(result2);
