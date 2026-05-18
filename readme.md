本仓库存放个人编写的实用脚本

## 脚本简介

下面简单介绍下几个脚本的作用和使用方法。


### 获取知乎无水印原图（Zhihu-get-the-original-image-without-watermark）

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

<br/>
<br/>
<br/>

### 去除知乎直达搜索链接（Zhihu-remove-Automatic-Keyword-Linking）

脚本地址：https://greasyfork.org/zh-CN/scripts/531190

源码地址：[点这里](./Zhihu-remove-Automatic-Keyword-Linking/main.js)

很多平台，都会自动将用户内容中的关键字，替换为超链接。

点击这些超链接，就会在平台内搜索该关键字，某种程度上算方便了用户，但也影响了美观以及保存。

开发思路：用正则匹配超链接，然后替换为纯文本。

以上两个脚本的详细说明，可参考我的个人博客：[写了两个实用的知乎油猴脚本（用 AI 两分钟搞定！） ](https://www.peterjxl.com/Browser/Tampermonkey-scripts/Two-scripts-for-zhihu-write-by-myself)

<br/>
<br/>
<br/>


### 在 EPUB 中加个空格（epub_add_space_between_cn_en）

平时有读书的习惯，但大部分书都没有在中文和英文（和数字）之间，加一个空格。降低了阅读体验。

为什么加个空格能提升阅读体验？看一个句子的对比：

1. 在中文句子里，出现嵌入English Words的情况。
2. 在中文句子里，出现嵌入“English Words”的情况。
3. 在中文句子里，出现嵌入 English Words 的情况。

对于第一个句子，明显可以感觉英文字符是被挤压在句子中的。而后面两个句子因为英文字符前后有一定的空隙，则不会有这种感觉。其实，如果你不认真去感受，或者平时不去注意它，也就没有那么「碍眼」。

所以，我就写了一个脚本，处理 EPUB 文件，在中文和英文字符之间加一个空格。

使用方法：

1. 先在 [Python 官网](https://www.python.org/) 下载安装 Python
2. 安装依赖库：`pip install beautifulsoup4`
3. 运行脚本：`python epub_add_space_between_cn_en.py input.epub output.epub`


后来，我还使用 Quicker 封装该命令，实现一键处理。


关于背景信息和开发过程，可以看我的这篇文章：[一个小技巧，让电子书阅读体验翻倍！](https://www.peterjxl.com/Reading/tools/add-a-blank/)

关于 Quicker，可以看我的这篇文章：[Quicker：我唯一愿意称之为神器的工具](https://www.peterjxl.com/Productive-Tool/Quicker)

<br/>
<br/>
<br/>

### 在 TXT 中加个空格（txt_add_space_between_cn_en）

该脚本用于在 txt 文件中加个空格。

使用方法：

1. 先在 [Python 官网](https://www.python.org/) 下载安装 Python
2. 安装依赖库：`pip install chardet`
3. 运行脚本
   1. 基础用法：`python txt_add_space_between_cn_en.py input.txt`
   2. 自定义输出路径：`python txt_add_space_between_cn_en.py input.txt -o output.txt`

同上，也可以用 Quicker 封装该命令，实现一键处理。

## 最后

欢迎试用和点赞~