var $j = jQuery.noConflict();

$j.fn.addHover = function() {
  return this.hover(function() {
    $j(this).addClass("hover")
  }, function() {
    $j(this).removeClass("hover")
  })
};

$j.fn.location = function() {
  var a = this;
  $j("a#set-location").click(function() {
    $j(this).parent().hide();
    a.show();
    $j("input#loc", a)[0].focus();
    return false
  })
};

var counter = {
  el: null,
  button: null,
  target: null,
  re: RegExp(/^\s*|\s*$/g),
  count: function() {
    var a = counter.el.value.replace(/\n/g, ""), b = a.length;
    chars_left = 256 - b;
    if (chars_left >= 0) {
      $j(counter.target.parentNode).is(".overlimit") && $j(counter.target.parentNode).removeClass("overlimit");
      str = chars_left > 1 ? "c\u00f2n " + chars_left + " k\u00fd t\u1ef1" : chars_left > 0 ? "c\u00f2n 1 k\u00fd t\u1ef1" : "v\u1eeba h\u1ebft s\u1ed1 k\u00fd t\u1ef1 cho ph\u00e9p"
    }
    else {
      $j(counter.target.parentNode).is(".overlimit") || $j(counter.target.parentNode).addClass("overlimit");
      str = chars_left < -1 ? "qu\u00e1 " + -chars_left + " k\u00fd t\u1ef1" : "qu\u00e1 1 k\u00fd t\u1ef1"
    }
    if ((b > 0 && b < 257 && a.replace(counter.re, "") != counter.el._value) == true) {
      ob = $j(".send-message-disable");
      ob.attr("onclick", "document.message_form.submit();");
      ob.attr("class", "send-message-enable")
    }
    counter.target.nodeValue = str
  }
};

$j.fn.presence = function() {
  var a = $j("textarea#message", this), b = $j(this).find("input[@type=submit]"), c = null;
  b.attr("disabled", true);
  this.icons();
  a.get(0)._value = a.attr("value");
  a.one("focus", function() {
    if (this.value == " ") {
      this.value = "";
      $j(this).css({
        color: "#000"
      })
    }
  });
  a.focus(function() {
    $j(this).css({
      color: "#000"
    });
    counter.el = this;
    counter.button = b.get(0);
    counter.target = $j("p#counter").get(0).firstChild;
    c = window.setInterval(counter.count, 500)
  });
  a.blur(function() {
    c && window.clearInterval(c)
  });
  this.submit(function() {
    if (b.attr("disabled")) {
      b.show();
      $j("span.loader", this).hide();
      b.attr("disabled", true);
      return false
    }
    var d = $j("input#loc");
    d.length > 0 && $j("input#location").attr("value", d.attr("value"));
    if (window.location.search.indexOf("?page") != 0) {
      $.ajax({
        type: "POST",
        url: this.action,
        data: $j("textarea, input, select", this).serialize(),
        success: function(e) {
          var f = document.createElement("div");
          f.innerHTML = e;
          e = $j("li", f);
          e.css("display", "none");
          if (e.size() > 0) {
            if ($j("div#stream li.date:first").length) {
              $j("div#stream li.date:first").after(e)
            }
            else {
              f = document.createElement("ul");
              f.className = "stream";
              $j("div#stream p:first").remove();
              $j("div#stream").prepend(f);
              $j("div#stream ul").append(e)
            }
            e.toggle()
          }
          else {
            alert("Hmm. C\u00f3 m\u1ed9t s\u1ed1 th\u1ee9 \u0111\u00e3 ho\u1ea1t \u0111\u1ed9ng kh\u00f4ng \u0111\u00fang nh\u01b0 mong mu\u1ed1n :(")
          }
          b.show();
          $j("span.loader", this).hide();
          b.attr("disabled", true)
        }
      });
      a.get(0)._value = a.attr("value");
      a.get(0).blur();
      a.css({
        color: "#ccc"
      });
      return false
    }
  })
};

$j.fn.spy = function() {
  var a = this;
  window.setInterval(function() {
    $.get(window.location.href, function(b) {
      a.find("ul").remove();
      a.append(b)
    })
  }, 3E4)
};

$j.fn.toggleable = function(a) {
  a = a;
  var b = this;
  $j("a[@href=#" + this.attr("id") + "]").click(function() {
    if (b.css("display") == "none") {
      a && $j(a).hide();
      b.show()
    }
    else {
      a && $j(a).show();
      b.hide()
    }
  })
};

$j.fn.toggleSelection = function(a, b) {
  var c = $j(a);
  this.click(function() {
    c.attr("checked", b ? true : false);
    return false
  })
};

$j.fn.icons = function() {
  var a = $j("a#add-icons", this), b = null, c = null, d = this;
  a.toggle(function() {
    if (!b) {
      var e = ['<div id="form-icons">'];
      $j("option", d).each(function() {
        if (this.value != "") {
          e.push('<label for="icon-' + this.value + '" title="' + this.title + '">');
          e.push('<img src="' + this.id + '" class="icon" alt="' + this.text + '" />');
          this.title != "" && e.push("<h4> " + this.title + " </h4>");
          e.push("</label>")
        }
      });
      e.push("</div>");
      d.append(e.join(""));
      b = $j("div#form-icons");
      $j("textarea#message").before('<img id="current-photo" class="icon"/>');
      c = $j("img#current-photo").hide();
      c.click(function() {
        a.click()
      });
      $j("label", b).click(function() {
        var f = $j(this).attr("for").replace("icon-", ""), g = 0;
        $j("select#icon>option").each(function(j) {
          if (this.value == f) {
            g = j
          }
        });
        $j("select#icon").get(0).selectedIndex = g;
        $j("label", b).removeClass("selected");
        $j(this).addClass("selected");
        c.attr("src", $j(this).find("img").get(0).src);
        c.css({
          display: "inline"
        });
        c.click();
        var i = $j("textarea#message");
        i.css({
          width: "349px"
        });
        if (i.size() > 0) {
          d = i.get(0);
          if (d._first) {
            d.value = this.title;
            d._first = null
          }
          d.focus()
        }
      })
    }
    b.show();
    $j(document.body).bind("click", function() {
      c.click()
    })
  }, function() {
    b.hide();
    $j(document.body).unbind("click")
  })
};

$j.fn.avatars = function() {
  var a = this, b = $j("img#current"), c = $j("button[@type='submit']");
  $j("label", a).click(function(d) {
    var e = $j("img", this).attr("src");
    $j("li", a).removeClass("selected");
    $j(this).parent().addClass("selected");
    $j(this).parent().find("input").get(0).checked = true;
    b.attr("src", e);
    c.attr("class", "active");
    d.preventDefault()
  })
};

$j.fn.backgrounds = function() {
  var a = this, b = $j("input#background");
  $j("label", a).click(function() {
    $j("li", a).removeClass("selected");
    $j(this).parent().addClass("selected");
    var c = $j("input", this).attr("value");
    b.attr("value", c);
    b.attr("name", "background");
    b.attr("checked", "checked")
  })
};

$j.fn.ajaxify = function() {
  this.click(function() {
    var a = $j(this).parent();
    a.html("vui l\u00f2ng ch\u1edd m\u1ed9t ch\u00fat...");
    $.ajax({
      type: "GET",
      url: this.href,
      success: function(b) {
        a.html(b)
      }
    });
    return false
  })
};
$j.fn.confirm = function() {
  this.click(function() {
    this.href += "&confirm=1";
    return window.confirm("B\u1ea1n ch\u1eafc ch\u1eafn mu\u1ed1n th\u1ef1c hi\u1ec7n thao t\u00e1c n\u00e0y?")
  })
};

$j.fn.setAccordion = function() {
  var a = this, b = a.find("li>a");
  a._current = null;
  b.click(function() {
    var c = this.hash.substring(1, this.hash.length);
    if (a._current == c) {
      $j("div#" + a._current).removeClass("current");
      a.find("ul li").removeClass("current");
      a.removeClass("open");
      a._current = null;
      return false
    }
    else {
      a._current && $j("div#" + a._current).removeClass("current")
    }
    $j("div#" + c).addClass("current").find("input[@type='text'], input[@type='file'], textarea").get(0).focus();
    a.find("ul li").removeClass("current");
    $j(this.parentNode).addClass("current");
    a._current = c;
    a.addClass("open");
    return false
  })
};

$j.fn.toggleCheckbox = function() {
  var a = $j(this.form).find("input[@name=" + this.attr("name") + "]");
  this.click(function() {
    var b = this.checked;
    a.each(function() {
      this.checked = false
    });
    this.checked = b ? true : false
  })
};

$j.fn.poll = function(a) {
  var b = window.location.href;
  window.setInterval(function() {
    $.ajax({
      type: "GET",
      url: b,
      dataType: "json",
      success: function(c) {
        if (c.result) {
          if (a) {
            window.location.href = a
          }
          else {
            window.location.reload()
          }
        }
      }
    })
  }, 2500)
};

$j.fn.setTabs = function() {
  var a = this;
  a.find("li>a").click(function() {
    var b = this.hash.substring(1, this.hash.length);
    $j("div#" + a._current).removeClass("current");
    $j("div#" + b).addClass("current");
    a.find("ul li").removeClass("current");
    $j(this.parentNode).addClass("current");
    a._current = b;
    return false
  });
  a._current = this.find("div.current").attr("id")
};

$j.fn.forms = function() {
  $j("input[@type=submit]", this).parent().prepend("<span class='loader' title='\u0110ang g\u1eedi...'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Processing...</span>");
  this.bind("submit", function() {
    $j("input[@type=submit]", this).hide();
    $j("span.cancel", this).hide();
    $j("span.loader", this).show()
  });
  this.each(function() {
    switch (this.id) {
      case "comment-form":
        $j("#participant-nicks > a", this).each(function() {
          $j(this).click(function() {
            var b = $j(this).text(), c = $j("#comment"), d = c.val(), e;
            c.focus();
            if (c.get(0).selectionStart == undefined) {
              e = document.selection.createRange();
              e = Array(e.start, e.end)
            }
            else {
              e = Array(c.get(0).selectionStart, c.get(0).selectionEnd)
            }
            e[0] === 0 ? c.val("@" + b + ": " + d.substring(e[1], d.length)) : c.val(d.substring(0, e[0]) + "@" + b + d.substring(e[1], d.length));
            return false
          })
        });
        $j("#participant-nicks").show();
        break;
      case "loginform":
        $j("input[@type=text]", this).get(0).focus();
        break;
      case "signup":
        $j("input[@type=text]", this).get(0).focus();
        var a = $j("input#password");
        a.parent().append('<div id="pwstatus"></div');
        a.bind("keyup", function() {
          analyseAccountPassword()
        });
        break;
      case "form-location":
        $j(this).location();
        break;
      case "form-design":
        $j(this).backgrounds();
        break;
      case "form-avatar":
        $j("div.avatars", this).avatars();
        if ($j("a#toggle").size() > 0) {
          $j("div.form-fields").hide();
          $j("a#toggle").click(function() {
            $j("div#account-form div.form-fields").show();
            $j(this).hide();
            return false
          })
        }
        break
    }
    switch (this.parentNode.id) {
      case "form-message":
        $j(this).presence();
        break
    }
  })
};

$j(document).ready(function() {
  $j.browser.msie && $j("ul#main-nav>li").addHover();
  var a = document.body, b = $j(a).css("background-color");
  if (!(b == "#ffffff" || b == "rbg(255,255,255)")) {
    $j("form").forms();
    b = $j("div#sidebar");
    
    $j("a.confirm-delete").confirm();
    $j("a.confirm-spam").confirm();
    $j("a.ajaxify").ajaxify();
    $j("div.tabs").setTabs();
    $j("div.accordion").setTabs();
    $j("form#change-number").toggleable("div#activation, div#activated");
    if (a.id == "welcome" || a.id == "contacts") {
      $j("a#select-all").toggleSelection("input[@name='actor[]'], input[@name='email[]']", true);
      $j("a#select-none").toggleSelection("input[@name='actor[]'], input[@name='email[]']", false)
    }
    a.id == "settings" && $j("ul#badges").length && initBadges();
    $j("input#only-channel, input#only-user").toggleCheckbox()
  }
});
if (!Array.prototype.indexOf) {
  Array.prototype.indexOf = function(a, b) {
    if (b == null) {
      b = 0
    }
    else {
      if (b < 0) {
        b = Math.max(0, this.length + b)
      }
    }
    for (var c = b; c < this.length; c++) {
      if (this[c] === a) {
        return c
      }
    }
    return -1
  }
}
var pwMinLen = 6, pwOkLen = 8, pwCut = 10;
function passwordStrength(a, b) {
  var c = 0;
  if (a.length > 0) {
    if (a.length >= pwMinLen) {
      a = a.substr(0, pwCut);
      var d = a.toLowerCase();
      c = 1;
      for (var e = false, f = 0; f < b.length; f++) {
        if (d.indexOf(b[f].substr(0, pwCut).toLowerCase()) != -1) {
          e = true;
          break
        }
      }
      if (!e) {
        a.length >= pwOkLen && c++;
        a.toLowerCase() != a && a.toUpperCase() != a && c++;
        a.search(/[0-9]/) != -1 && a.search(/[A-Za-z]/) != -1 && c++;
        a.search(/[^0-9A-Za-z]/) != -1 && c++;
        if (c > 4) {
          c = 4
        }
      }
    }
  }
  else {
    c = -1
  }
  return c
}

function analyseAccountPassword(a) {
  var b = document.getElementById("password").value, c = document.getElementById("pwstatus");
  if (c || a) {
    ban = [];
    var d = document.getElementById("nick");
    d && d.value && ban.push(d.value);
    (d = document.getElementById("email")) && d.value && ban.push(d.value);
    (d = document.getElementById("full_name")) && d.value && ban.push(d.value);
    (d = document.getElementById("city")) && d.value && ban.push(d.value);
    b = passwordStrength(b, ban);
    c.style.backgroundPosition = "0px " + (-b * 20 - 20) + "px";
    if (a) {
      return b
    }
  }
}

function checkPassword(a) {
  if (a.length < 8) {
    return false
  }
  if (a.search(/[A-Z]/) == -1) {
    return false
  }
  if (a.search(/[a-z]/) == -1) {
    return false
  }
  if (a.search(/[0-9]/) == -1) {
    return false
  }
  return true
}

function getFieldValue(a) {
  if ((a = document.getElementById(a)) && a.value) {
    return a.value
  }
  return ""
}

function getOffset(a) {
  for (var b = 0, c = 0; a.offsetParent;) {
    b += a.offsetTop || 0;
    c += a.offsetLeft || 0;
    a = a.offsetParent
  }
  return [c, b]
}

$j(function() {
  setTimeout(function() {
    $j("#notice").fadeOut(300)
  }, 3E3)
});


$j(document).ready(function($) {
  $j("body").fadeIn(300);
  
  $j(document.body).click(function(event) {
    if ((event.target.nodeName == "A" &&
    event.target.className != "send-message-disable" &&
    event.target.className != "disable-fadeout" &&
    event.target.target != "_new" &&
    event.target.target != "_blank") ||
    (event.target.nodeName == "IMG" &&
    event.target.className == "photo") ||
    (event.target.type == "submit" &&
    event.target.name != "submit-location") ||
    (event.target.nodeName == "SPAN" &&
    event.target.className != "nickname" &&
    event.target.className != "full-name" &&
    event.target.className != "disable-fadeout")) {
      $j(document.body).fadeOut(500)
    }
  })
})
