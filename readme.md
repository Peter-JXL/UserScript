本仓库存放个人编写的实用脚本（包含油猴脚本和 Python 脚本等）。

## 脚本简介

下面简单介绍下几个脚本。


### 获取知乎无水印原图

脚本地址：https://greasyfork.org/zh-CN/scripts/531189

源码地址：[点这里](./Zhihu-get-the-original-image-without-watermark/main.js)


在知乎，默认情况下，用户上传的图片都是自动在右下角添加水印的（可以在设置 — 偏好设置里取消）。

如果你查看网页源代码（F12），定位到图片，你会发现代码长这样，有很多的属性：

```html
<img src="https://pic3.zhimg.com/v2-954903cb202300124413cf4c17222d54_1440w.jpg" 
     data-size="normal" 
     data-rawwidth="2292" 
     data-rawheight="1438" 
     data-original-token="v2-6c6a915346f4010e25e6989964e6d5ca" 
     class="origin_image zh-lightbox-thumb" 
     width="2292" 
     data-original="https://pic3.zhimg.com/v2-954903cb202300124413cf4c17222d54_r.jpg" 
     title="" style=""
 >
```

src 属性的值是图片链接（带用户水印的）。而 `data-original-token` 属性的值，和 src 里的图片文件名很相似，尝试用其替换掉 src 属性里的文件名，得到了无水印的原图。

所以，开发思路就是，遍历网页上的所有图片，用 `data-original-token` 属性的值替换掉 src 属性值的文件名。

经实测，和部分知乎相关的脚本冲突，目前还在研究中。





### 去除知乎直达搜索链接

脚本地址：https://greasyfork.org/zh-CN/scripts/531190

源码地址：[点这里](./Zhihu-remove-Automatic-Keyword-Linking/main.js)

很多平台，都会自动将用户内容中的关键字，替换为超链接。

点击这些超链接，就会在平台内搜索该关键字，某种程度上算方便了用户，但也影响了美观以及保存。

开发思路：用正则匹配超链接，然后替换为纯文本。

由于我不怎么保存其他平台的内容，所以该脚本仅针对知乎。

---

以上两个脚本的详细说明，请参考我的个人博客：[写了两个实用的知乎油猴脚本（用 AI 两分钟搞定！） ](https://www.peterjxl.com/Browser/Tampermonkey-scripts/Two-scripts-for-zhihu-write-by-myself)




### 在 EPUB 中加个空格

源码地址：[点这里](./epub_add_space_between_cn_en/epub_add_space_between_cn_en.py)

平时有读书的习惯（也偶尔看看网文），但大部分书都没「加个空格」，对于我这个习惯了加空格的人来说，阅读体验很不好。

什么是加个空格？简单来说，就是在中文和英文（和数字）之间，加一个空格。

下面进行一个句子对比：

1. 在中文句子里，出现嵌入English Words的情况。
2. 在中文句子里，出现嵌入“English Words”的情况。
3. 在中文句子里，出现嵌入 English Words 的情况。

对于第一个句子，明显可以感觉英文字符是被挤压在句子中的。而后面两个句子因为英文字符前后有一定的空隙，则不会有这种感觉。其实，如果你不认真去感受，或者平时不去注意它，也就没有那么「碍眼」。

所以，我就写了一个脚本，处理 EPUB 文件，在中文和英文字符之间加一个空格。

后来，我还使用 Quicker 封装该命令，实现一键处理。

更多内容，请参考：[一个小技巧，让电子书阅读体验翻倍！](https://www.peterjxl.com/Reading/tools/add-a-blank/)



## 最后

欢迎使用和点赞~