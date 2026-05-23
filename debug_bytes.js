// 直接查看解密后的字节数据
function debugDecrypt(encryptedUrl) {
    for (let offset = 1; offset < 20; offset++) {
        try {
            const testStr = encryptedUrl.substring(offset);
            const decoded = Buffer.from(testStr, 'base64');
            const decodedStr = decoded.toString('utf8');
            
            if (decodedStr.includes('.m3u8')) {
                console.log('==================');
                console.log('偏移: ' + offset);
                console.log('字节长度: ' + decoded.length);
                console.log();
                console.log('字符串表示:');
                console.log(decodedStr);
                console.log();
                console.log('字符编码:');
                for (let i = 0; i < Math.min(100, decoded.length); i++) {
                    let charInfo = String.fromCharCode(decoded[i]);
                    if (charInfo === '\n' || charInfo === '\r') charInfo = '\\n';
                    if (charInfo === '\t') charInfo = '\\t';
                    if (decoded[i] < 32 || decoded[i] > 126) {
                        console.log(i + ': 0x' + decoded[i].toString(16).padStart(2, '0') + ' (invalid)');
                    } else {
                        console.log(i + ': 0x' + decoded[i].toString(16).padStart(2, '0') + ' ' + charInfo);
                    }
                }
                console.log();
                
                // 找到第一个看起来正常的路径开始
                let startIdx = -1;
                for (let i = 0; i < decoded.length - 10; i++) {
                    // 找一个看起来正常的序列开始，比如数字或字母
                    let validCount = 0;
                    for (let j = 0; j < 30; j++) {
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
                    // 如果有25个以上的有效字符，可能就是这里开始
                    if (validCount >= 25) {
                        startIdx = i;
                        break;
                    }
                }
                
                if (startIdx !== -1) {
                    // 从startIdx开始，提取到.m3u8+5的位置
                    const tempStr = decoded.toString('utf8', startIdx);
                    const m3u8Pos = tempStr.indexOf('.m3u8');
                    if (m3u8Pos !== -1) {
                        const cleanPath = tempStr.substring(0, m3u8Pos + 5);
                        console.log('可能的路径:');
                        console.log('https://play.svip30.tv/' + cleanPath);
                    }
                }
                break;
            }
        } catch (e) {}
    }
}

// 测试综艺URL
var varietyUrl = 'aFHBRI09c7H3M16HLeyl9l2oaWXrAouhbdH0o8t2Y42JR3u4M7T8IZu0Y82D9etSL0zIwMjMwMzIxLzYzOTNfMWU3MWM0MzEvaW5kZXgubTN1OAO0O0OO0O0O';
console.log('调试综艺URL...');
debugDecrypt(varietyUrl);
