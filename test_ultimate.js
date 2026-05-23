// 终极版解密函数 - 超级精确
function decryptVideoUrl(encryptedUrl) {
    try {
        for (let offset = 1; offset < 20; offset++) {
            try {
                const testStr = encryptedUrl.substring(offset);
                const decoded = Buffer.from(testStr, 'base64');
                
                let startPos = -1;
                // 直接找第一个数字字符，因为所有路径都是从数字开始的
                for (let i = 0; i < decoded.length; i++) {
                    if (decoded[i] >= 48 && decoded[i] <= 57) {
                        // 检查这个数字开始的路径是否有至少两个 / 和 .m3u8
                        let slashCount = 0;
                        let hasM3u8 = false;
                        
                        for (let j = i; j < Math.min(i + 100, decoded.length); j++) {
                            if (decoded[j] === 47) slashCount++;
                            
                            // 检查是否是 .m3u8
                            if (j >= i + 4) {
                                if (decoded[j-4] === 46 && 
                                    decoded[j-3] === 109 && 
                                    decoded[j-2] === 51 && 
                                    decoded[j-1] === 117 && 
                                    decoded[j] === 56) {
                                    hasM3u8 = true;
                                    break;
                                }
                            }
                        }
                        
                        if (slashCount >= 2 && hasM3u8) {
                            startPos = i;
                            break;
                        }
                    }
                }
                
                if (startPos !== -1) {
                    const tempStr = decoded.toString('utf8', startPos);
                    const m3u8Pos = tempStr.indexOf('.m3u8');
                    if (m3u8Pos !== -1) {
                        const cleanPath = tempStr.substring(0, m3u8Pos + 5);
                        return 'https://play.svip30.tv/' + cleanPath;
                    }
                }
            } catch (e) {}
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
