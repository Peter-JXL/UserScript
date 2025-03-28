// ==UserScript==
// @name         知乎-获取无水印原图
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  获取知乎无水印图片，并替换掉页面上的有水印图片
// @icon         https://s21.ax1x.com/2025/03/23/pE0qpRK.jpg
// @compatible   chrome,edge,firefox
// @author       PeterJXL
// @homepageURL  https://www.peterjxl.com
// @license      MIT
// @create       2025-03-28
// @lastmodified 2025-03-28
// @match        https://www.zhihu.com/*
// @match        https://zhuanlan.zhihu.com/*
// @run-at       document-end
// @supportURL   https://github.com/Peter-JXL/UserScript/issues
// @grant        none
// @note         可能会和其他知乎脚本冲突，例如「知乎美化」，还在调试中
// ==/UserScript==


(function () {
  'use strict';

  // 原理：知乎的 Img 标签中，有个 data-original-token 属性，值为无水印图片的文件名。先获取它，再替换掉 Img 标签的 src 属性中的图片文件名，即可显示无水印图片。
  function getOriginalImgAndReplace() {
    const images = document.querySelectorAll('img[data-original-token]');
    images.forEach(img => {
      const newToken = img.dataset.originalToken;
      const newSrc = img.src.replace(/v2-[a-f0-9]+(?=_)/, newToken);
      if (newSrc !== img.src) {
        img.src = newSrc;
      }
    });
  }

  // 初始执行
  getOriginalImgAndReplace();

  // 监听动态加载的图片（如滚动加载）
  const observer = new MutationObserver(getOriginalImgAndReplace);
  observer.observe(document.body, { childList: true, subtree: true });

})();