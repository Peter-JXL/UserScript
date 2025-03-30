本仓库存放个人编写的油猴脚本。

## 脚本简介

目前有 2 个脚本，简单介绍下：



### 获取知乎无水印原图

脚本地址：https://greasyfork.org/zh-CN/scripts/531189

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

经实测，可能会和其他知乎相关的脚本冲突，目前还在研究中。



### 去除知乎直达搜索链接

脚本地址：https://greasyfork.org/zh-CN/scripts/531190

很多平台，都会自动将用户内容中的关键字，替换为超链接。

点击这些超链接，就会在平台内搜索该关键字，某种程度上算方便了用户，但也影响了美观以及保存。

开发思路：用正则匹配超链接，然后替换为纯文本。

由于我不怎么保存其他平台的内容，所以该脚本仅针对知乎。

---

以上两个脚本的详细说明，请参考我的个人博客：[写了两个实用的知乎油猴脚本（用 AI 两分钟搞定！） ](https://www.peterjxl.com/Browser/Tampermonkey-scripts/Two-scripts-for-zhihu-write-by-myself)



## 最后

欢迎试用和点赞~