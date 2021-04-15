$(document).ready(function () {
  bindToolBarEvent();
  // bindSummaryActive();
  bindScrollTo();
  // bindSummaryTo();
});

/*
 *  判断用户访问的设备 PC OR MOBILE
 */
function isPc() {
  var userAgent = navigator.userAgent.toLowerCase();
  var bIsIpad = userAgent.match(/ipad/i) == "ipad";
  var bIsIphoneOs = userAgent.match(/iphone os/i) == "iphone os";
  var bIsMidp = userAgent.match(/midp/i) == "midp";
  var bIsUc7 = userAgent.match(/rv:1.2.3.4/i) == "rv:1.2.3.4";
  var bIsUc = userAgent.match(/ucweb/i) == "ucweb";
  var bIsAndroid = userAgent.match(/android/i) == "android";
  var bIsCE = userAgent.match(/windows ce/i) == "windows ce";
  var bIsWM = userAgent.match(/windows mobile/i) == "windows mobile";

  if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
    return false;
  } else {
    return true;
  }
}

/*
 *  菜单栏拉伸效果
 */
function bindToolBarEvent() {

  //$("img.js-toolbar-action2").click(function () {
  $("i.fa-align-justify").click(function () {
    var toggleClassEle = $(".book-summary");

    function toggleStyle(isToggle) {
      if (isToggle){
        $(".book-body").css({"left": "0"});
        toggleClassEle.css({"left": "-100%"});
      }else{
        $(".book-body").css({"left": "300px"});
        toggleClassEle.css({"left": "0"});
      }
    }

    if (isPc()) {
      toggleClassEle.toggleClass("left");

      if (toggleClassEle.hasClass("left")) {
        toggleStyle(true);
      } else {
        toggleStyle(false);
      }
    }else {
      toggleClassEle.parent().toggleClass("with-summary");

      if (toggleClassEle.parent().hasClass("with-summary")) {
        toggleStyle(false);
      } else {
        toggleStyle(true);
      }
    }
  });

}

/*
 *  选中效果添加 `active`
 */
function bindSummaryActive() {
  $(".summary a").each(function () {
    const pathName = window.location.pathname;
    const elePath = $(this).attr("href");

    if (pathName === elePath) {
      $(this).parent().addClass("active").siblings().removeClass("active");
      $(this).parent().parent().css({"display": "block"});
    }
  })
}

/*
 *  初始化导航栏到指定高度
 */
function bindScrollTo() {
  let summary = $(".book-summary");
  let activeItem = summary.find(".chapter.active");

  if (activeItem.offset().top > document.documentElement.clientHeight) {
    // 可调整数值, 进行缓慢动画效果
    summary.animate({
      scrollTop: activeItem.offset().top - summary.offset().top + summary.scrollTop()
    }, 0);
  }
}

/*
 *  点击切换文章目录
 */

function bindSummaryTo() {
  $("[data-path]").click(function () {

    const reqHref = $(this).attr("href");
    history.pushState(null, null, reqHref);

    bindSummaryActive();

    $.ajax({
      url: '',
      method: "GET",
      dataType: "html",
      cache: !0,
      success: function (h) {
        $(".page-inner").html(h);
      }
    });

    return false;
  });
}
