if (typeof Object.create !== 'function') {
    Object.create = function (o) {
        function F() {
        }

        F.prototype = o;
        return new F();
    };
}
(function ($) {
    var NotyObject = {
        init: function (options) {
            this.options = $.extend({}, $.noty.defaults, options);
            this.options.layout = (this.options.custom) ? $.noty.layouts['inline'] : $.noty.layouts[this.options.layout];
            if ($.noty.themes[this.options.theme])
                this.options.theme = $.noty.themes[this.options.theme]; else
                options.themeClassName = this.options.theme;
            delete options.layout;
            delete options.theme;
            this.options = $.extend({}, this.options, this.options.layout.options);
            this.options.id = 'noty_' + (new Date().getTime() * Math.floor(Math.random() * 1000000));
            this.options = $.extend({}, this.options, options);
            this._build();
            return this;
        }, _build: function () {
            var $bar = $('<div class="noty_bar noty_type_' + this.options.type + '"></div>').attr('id', this.options.id);
            $bar.append(this.options.template).find('.noty_text').html(this.options.text);
            this.$bar = (this.options.layout.parent.object !== null) ? $(this.options.layout.parent.object).css(this.options.layout.parent.css).append($bar) : $bar;
            if (this.options.themeClassName)
                this.$bar.addClass(this.options.themeClassName).addClass('noty_container_type_' + this.options.type);
            if (this.options.buttons) {
                this.options.closeWith = [];
                this.options.timeout = false;
                var $buttons = $('<div/>').addClass('noty_buttons');
                (this.options.layout.parent.object !== null) ? this.$bar.find('.noty_bar').append($buttons) : this.$bar.append($buttons);
                var self = this;
                $.each(this.options.buttons, function (i, button) {
                    var $button = $('<button/>').addClass((button.addClass) ? button.addClass : 'gray').html(button.text).attr('id', button.id ? button.id : 'button-' + i).appendTo(self.$bar.find('.noty_buttons')).on('click', function () {
                        if ($.isFunction(button.onClick)) {
                            button.onClick.call($button, self);
                        }
                    });
                });
            }
            this.$message = this.$bar.find('.noty_message');
            this.$closeButton = this.$bar.find('.noty_close');
            this.$buttons = this.$bar.find('.noty_buttons');
            $.noty.store[this.options.id] = this;
        }, show: function () {
            var self = this;
            (self.options.custom) ? self.options.custom.find(self.options.layout.container.selector).append(self.$bar) : $(self.options.layout.container.selector).append(self.$bar);
            if (self.options.theme && self.options.theme.style)
                self.options.theme.style.apply(self);
            ($.type(self.options.layout.css) === 'function') ? this.options.layout.css.apply(self.$bar) : self.$bar.css(this.options.layout.css || {});
            self.$bar.addClass(self.options.layout.addClass);
            self.options.layout.container.style.apply($(self.options.layout.container.selector));
            self.showing = true;
            if (self.options.theme && self.options.theme.style)
                self.options.theme.callback.onShow.apply(this);
            if ($.inArray('click', self.options.closeWith) > -1)
                self.$bar.css('cursor', 'pointer').one('click', function (evt) {
                    self.stopPropagation(evt);
                    if (self.options.callback.onCloseClick) {
                        self.options.callback.onCloseClick.apply(self);
                    }
                    self.close();
                });
            if ($.inArray('hover', self.options.closeWith) > -1)
                self.$bar.one('mouseenter', function () {
                    self.close();
                });
            if ($.inArray('button', self.options.closeWith) > -1)
                self.$closeButton.one('click', function (evt) {
                    self.stopPropagation(evt);
                    self.close();
                });
            if ($.inArray('button', self.options.closeWith) == -1)
                self.$closeButton.remove();
            if (self.options.callback.onShow)
                self.options.callback.onShow.apply(self);
            self.$bar.animate(self.options.animation.open, self.options.animation.speed, self.options.animation.easing, function () {
                if (self.options.callback.afterShow)self.options.callback.afterShow.apply(self);
                self.showing = false;
                self.shown = true;
            });
            if (self.options.timeout)
                self.$bar.delay(self.options.timeout).promise().done(function () {
                    self.close();
                });
            return this;
        }, close: function () {
            if (this.closed)return;
            if (this.$bar && this.$bar.hasClass('i-am-closing-now'))return;
            var self = this;
            if (this.showing) {
                self.$bar.queue(function () {
                    self.close.apply(self);
                });
                return;
            }
            if (!this.shown && !this.showing) {
                var queue = [];
                $.each($.noty.queue, function (i, n) {
                    if (n.options.id != self.options.id) {
                        queue.push(n);
                    }
                });
                $.noty.queue = queue;
                return;
            }
            self.$bar.addClass('i-am-closing-now');
            if (self.options.callback.onClose) {
                self.options.callback.onClose.apply(self);
            }
            self.$bar.clearQueue().stop().animate(self.options.animation.close, self.options.animation.speed, self.options.animation.easing, function () {
                if (self.options.callback.afterClose)self.options.callback.afterClose.apply(self);
            }).promise().done(function () {
                if (self.options.modal) {
                    $.notyRenderer.setModalCount(-1);
                    if ($.notyRenderer.getModalCount() == 0)$('.noty_modal').fadeOut('fast', function () {
                        $(this).remove();
                    });
                }
                $.notyRenderer.setLayoutCountFor(self, -1);
                if ($.notyRenderer.getLayoutCountFor(self) == 0)$(self.options.layout.container.selector).remove();
                if (typeof self.$bar !== 'undefined' && self.$bar !== null) {
                    self.$bar.remove();
                    self.$bar = null;
                    self.closed = true;
                }
                delete $.noty.store[self.options.id];
                if (self.options.theme.callback && self.options.theme.callback.onClose) {
                    self.options.theme.callback.onClose.apply(self);
                }
                if (!self.options.dismissQueue) {
                    $.noty.ontap = true;
                    $.notyRenderer.render();
                }
                if (self.options.maxVisible > 0 && self.options.dismissQueue) {
                    $.notyRenderer.render();
                }
            })
        }, setText: function (text) {
            if (!this.closed) {
                this.options.text = text;
                this.$bar.find('.noty_text').html(text);
            }
            return this;
        }, setType: function (type) {
            if (!this.closed) {
                this.options.type = type;
                this.options.theme.style.apply(this);
                this.options.theme.callback.onShow.apply(this);
            }
            return this;
        }, setTimeout: function (time) {
            if (!this.closed) {
                var self = this;
                this.options.timeout = time;
                self.$bar.delay(self.options.timeout).promise().done(function () {
                    self.close();
                });
            }
            return this;
        }, stopPropagation: function (evt) {
            evt = evt || window.event;
            if (typeof evt.stopPropagation !== "undefined") {
                evt.stopPropagation();
            }
            else {
                evt.cancelBubble = true;
            }
        }, closed: false, showing: false, shown: false
    };
    $.notyRenderer = {};
    $.notyRenderer.init = function (options) {
        var notification = Object.create(NotyObject).init(options);
        if (notification.options.killer)
            $.noty.closeAll();
        (notification.options.force) ? $.noty.queue.unshift(notification) : $.noty.queue.push(notification);
        $.notyRenderer.render();
        return ($.noty.returns == 'object') ? notification : notification.options.id;
    };
    $.notyRenderer.render = function () {
        var instance = $.noty.queue[0];
        if ($.type(instance) === 'object') {
            if (instance.options.dismissQueue) {
                if (instance.options.maxVisible > 0) {
                    if ($(instance.options.layout.container.selector + ' li').length < instance.options.maxVisible) {
                        $.notyRenderer.show($.noty.queue.shift());
                    }
                    else {
                    }
                }
                else {
                    $.notyRenderer.show($.noty.queue.shift());
                }
            }
            else {
                if ($.noty.ontap) {
                    $.notyRenderer.show($.noty.queue.shift());
                    $.noty.ontap = false;
                }
            }
        }
        else {
            $.noty.ontap = true;
        }
    };
    $.notyRenderer.show = function (notification) {
        if (notification.options.modal) {
            $.notyRenderer.createModalFor(notification);
            $.notyRenderer.setModalCount(+1);
        }
        if (notification.options.custom) {
            if (notification.options.custom.find(notification.options.layout.container.selector).length == 0) {
                notification.options.custom.append($(notification.options.layout.container.object).addClass('i-am-new'));
            }
            else {
                notification.options.custom.find(notification.options.layout.container.selector).removeClass('i-am-new');
            }
        }
        else {
            if ($(notification.options.layout.container.selector).length == 0) {
                $('body').append($(notification.options.layout.container.object).addClass('i-am-new'));
            }
            else {
                $(notification.options.layout.container.selector).removeClass('i-am-new');
            }
        }
        $.notyRenderer.setLayoutCountFor(notification, +1);
        notification.show();
    };
    $.notyRenderer.createModalFor = function (notification) {
        if ($('.noty_modal').length == 0) {
            var modal = $('<div/>').addClass('noty_modal').addClass(notification.options.theme).data('noty_modal_count', 0);
            if (notification.options.theme.modal && notification.options.theme.modal.css)
                modal.css(notification.options.theme.modal.css);
            modal.prependTo($('body')).fadeIn('fast');
        }
    };
    $.notyRenderer.getLayoutCountFor = function (notification) {
        return $(notification.options.layout.container.selector).data('noty_layout_count') || 0;
    };
    $.notyRenderer.setLayoutCountFor = function (notification, arg) {
        return $(notification.options.layout.container.selector).data('noty_layout_count', $.notyRenderer.getLayoutCountFor(notification) + arg);
    };
    $.notyRenderer.getModalCount = function () {
        return $('.noty_modal').data('noty_modal_count') || 0;
    };
    $.notyRenderer.setModalCount = function (arg) {
        return $('.noty_modal').data('noty_modal_count', $.notyRenderer.getModalCount() + arg);
    };
    $.fn.noty = function (options) {
        options.custom = $(this);
        return $.notyRenderer.init(options);
    };
    $.noty = {};
    $.noty.queue = [];
    $.noty.ontap = true;
    $.noty.layouts = {};
    $.noty.themes = {};
    $.noty.returns = 'object';
    $.noty.store = {};
    $.noty.get = function (id) {
        return $.noty.store.hasOwnProperty(id) ? $.noty.store[id] : false;
    };
    $.noty.close = function (id) {
        return $.noty.get(id) ? $.noty.get(id).close() : false;
    };
    $.noty.setText = function (id, text) {
        return $.noty.get(id) ? $.noty.get(id).setText(text) : false;
    };
    $.noty.setType = function (id, type) {
        return $.noty.get(id) ? $.noty.get(id).setType(type) : false;
    };
    $.noty.clearQueue = function () {
        $.noty.queue = [];
    };
    $.noty.closeAll = function () {
        $.noty.clearQueue();
        $.each($.noty.store, function (id, noty) {
            noty.close();
        });
    };
    var windowAlert = window.alert;
    $.noty.consumeAlert = function (options) {
        window.alert = function (text) {
            if (options)
                options.text = text; else
                options = {text: text};
            $.notyRenderer.init(options);
        };
    };
    $.noty.stopConsumeAlert = function () {
        window.alert = windowAlert;
    };
    $.noty.defaults = {
        layout: 'top',
        theme: 'defaultTheme',
        type: 'alert',
        text: '',
        dismissQueue: true,
        template: '<div class="noty_message"><span class="noty_text"></span><div class="noty_close"></div></div>',
        animation: {open: {height: 'toggle'}, close: {height: 'toggle'}, easing: 'swing', speed: 500},
        timeout: false,
        force: false,
        modal: false,
        maxVisible: 5,
        killer: false,
        closeWith: ['click'],
        callback: {
            onShow: function () {
            }, afterShow: function () {
            }, onClose: function () {
            }, afterClose: function () {
            }, onCloseClick: function () {
            }
        },
        buttons: false
    };
    $(window).on('resize', function () {
        $.each($.noty.layouts, function (index, layout) {
            layout.container.style.apply($(layout.container.selector));
        });
    });
})(jQuery);
window.noty = function noty(options) {
    return jQuery.notyRenderer.init(options);
};
(function ($) {
    $.noty.themes.defaultTheme = {
        name: 'defaultTheme',
        helpers: {
            borderFix: function () {
                if (this.options.dismissQueue) {
                    var selector = this.options.layout.container.selector + ' ' + this.options.layout.parent.selector;
                    switch (this.options.layout.name) {
                        case'top':
                            $(selector).css({borderRadius: '0px 0px 0px 0px'});
                            $(selector).last().css({borderRadius: '0px 0px 5px 5px'});
                            break;
                        case'topCenter':
                        case'topLeft':
                        case'topRight':
                        case'bottomCenter':
                        case'bottomLeft':
                        case'bottomRight':
                        case'center':
                        case'centerLeft':
                        case'centerRight':
                        case'inline':
                            $(selector).css({borderRadius: '0px 0px 0px 0px'});
                            $(selector).first().css({
                                'border-top-left-radius': '0px',
                                'border-top-right-radius': '0px'
                            });
                            $(selector).last().css({
                                'border-bottom-left-radius': '0px',
                                'border-bottom-right-radius': '0px'
                            });
                            break;
                        case'bottom':
                            $(selector).css({borderRadius: '0px 0px 0px 0px'});
                            $(selector).first().css({borderRadius: '5px 5px 0px 0px'});
                            break;
                        default:
                            break;
                    }
                }
            }
        },
        modal: {
            css: {
                position: 'fixed',
                width: '100%',
                height: '100%',
                backgroundColor: '#000',
                zIndex: 10000,
                opacity: 0.6,
                display: 'none',
                left: 0,
                top: 0
            }
        },
        style: function () {
            this.$bar.css({overflow: 'hidden'});
            this.$message.css({
                fontSize: '16px',
                lineHeight: '22px',
                textAlign: 'center',
                padding: '12px 15px 13px',
                width: 'auto',
                position: 'relative'
            });
            this.$closeButton.css({
                position: 'absolute',
                top: 4,
                right: 4,
                width: 10,
                height: 10,
                display: 'none',
                cursor: 'pointer'
            });
            this.$buttons.css({padding: 5, textAlign: 'right', borderTop: '1px solid #ccc', backgroundColor: '#fff'});
            this.$buttons.find('button').css({marginLeft: 5});
            this.$buttons.find('button:first').css({marginLeft: 0});
            this.$bar.on({
                mouseenter: function () {
                    $(this).find('.noty_close').stop().fadeTo('normal', 1);
                }, mouseleave: function () {
                    $(this).find('.noty_close').stop().fadeTo('normal', 0);
                }
            });
            switch (this.options.layout.name) {
                case'top':
                    this.$bar.css({
                        borderRadius: '0px 0px 5px 5px',
                        borderBottom: '2px solid #eee',
                        borderLeft: '2px solid #eee',
                        borderRight: '2px solid #eee',
                        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)"
                    });
                    break;
                case'topCenter':
                case'center':
                case'bottomCenter':
                case'inline':
                    this.$bar.css({
                        borderRadius: '5px',
                        border: '1px solid #eee',
                        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)"
                    });
                    this.$message.css({fontSize: '16px', textAlign: 'center'});
                    break;
                case'topLeft':
                case'topRight':
                case'bottomLeft':
                case'bottomRight':
                case'centerLeft':
                case'centerRight':
                    this.$bar.css({
                        borderRadius: '5px',
                        border: '1px solid #eee',
                        boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)"
                    });
                    this.$message.css({fontSize: '13px', textAlign: 'left'});
                    break;
                case'bottom':
                    this.$bar.css({
                        borderRadius: '5px 5px 0px 0px',
                        borderTop: '2px solid #eee',
                        borderLeft: '2px solid #eee',
                        borderRight: '2px solid #eee',
                        boxShadow: "0 -2px 4px rgba(0, 0, 0, 0.1)"
                    });
                    break;
                default:
                    this.$bar.css({border: '2px solid #eee', boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)"});
                    break;
            }
            switch (this.options.type) {
                case'alert':
                case'notification':
                    this.$bar.css({backgroundColor: '#FFF', borderColor: '#CCC', color: '#444'});
                    break;
                case'warning':
                    this.$bar.css({backgroundColor: '#FFEAA8', borderColor: '#FFC237', color: '#826200'});
                    this.$buttons.css({borderTop: '1px solid #FFC237'});
                    break;
                case'error':
                    this.$bar.css({backgroundColor: 'red', borderColor: 'darkred', color: '#FFF'});
                    this.$buttons.css({borderTop: '1px solid darkred'});
                    break;
                case'information':
                    this.$bar.css({backgroundColor: '#57B7E2', borderColor: '#0B90C4', color: '#FFF'});
                    this.$buttons.css({borderTop: '1px solid #0B90C4'});
                    break;
                case'success':
                    this.$bar.css({backgroundColor: 'white', borderColor: '#044878', color: '#055995'});
                    break;
                default:
                    this.$bar.css({backgroundColor: '#FFF', borderColor: '#CCC', color: '#444'});
                    break;
            }
        },
        callback: {
            onShow: function () {
                $.noty.themes.defaultTheme.helpers.borderFix.apply(this);
            }, onClose: function () {
                $.noty.themes.defaultTheme.helpers.borderFix.apply(this);
            }
        }
    };
})(jQuery);
(function ($) {
    $.noty.layouts.center = {
        name: 'center', options: {}, container: {
            object: '<ul id="noty_center_layout_container" />',
            selector: 'ul#noty_center_layout_container',
            style: function () {
                $(this).css({
                    position: 'fixed',
                    width: '310px',
                    height: 'auto',
                    margin: 0,
                    padding: 0,
                    listStyleType: 'none',
                    zIndex: 10000000
                });
                var dupe = $(this).clone().css({
                    visibility: "hidden",
                    display: "block",
                    position: "absolute",
                    top: 0,
                    left: 0
                }).attr('id', 'dupe');
                $("body").append(dupe);
                dupe.find('.i-am-closing-now').remove();
                dupe.find('li').css('display', 'block');
                var actual_height = dupe.height();
                dupe.remove();
                if ($(this).hasClass('i-am-new')) {
                    $(this).css({
                        left: ($(window).width() - $(this).outerWidth(false)) / 2 + 'px',
                        top: ($(window).height() - actual_height) / 2 + 'px'
                    });
                }
                else {
                    $(this).animate({
                        left: ($(window).width() - $(this).outerWidth(false)) / 2 + 'px',
                        top: ($(window).height() - actual_height) / 2 + 'px'
                    }, 500);
                }
            }
        }, parent: {object: '<li />', selector: 'li', css: {}}, css: {display: 'none', width: '310px'}, addClass: ''
    };
})(jQuery);
Event = (function () {
    var guid = 0;

    function fixEvent(event) {
        event = event || window.event;
        if (event.isFixed) {
            return event;
        }
        event.isFixed = true;
        event.preventDefault = event.preventDefault || function () {
                this.returnValue = false;
            };
        event.stopPropagation = event.stopPropagaton || function () {
                this.cancelBubble = true;
            };
        if (!event.target) {
            event.target = event.srcElement;
        }
        if (!event.relatedTarget && event.fromElement) {
            event.relatedTarget = event.fromElement === event.target ? event.toElement : event.fromElement;
        }
        if (event.pageX === null && event.clientX !== null) {
            var html = document.documentElement, body = document.body;
            event.pageX = event.clientX + (html && html.scrollLeft || body && body.scrollLeft || 0) - (html.clientLeft || 0);
            event.pageY = event.clientY + (html && html.scrollTop || body && body.scrollTop || 0) - (html.clientTop || 0);
        }
        if (!event.which && event.button) {
            event.which = (event.button && 1 ? 1 : (event.button && 2 ? 3 : (event.button && 4 ? 2 : 0)));
        }
        return event;
    }

    function commonHandle(event) {
        event = fixEvent(event);
        var handlers = this.events[event.type];
        for (var g in handlers) {
            var handler = handlers[g];
            var ret = handler.call(this, event);
            if (ret === false) {
                event.preventDefault();
                event.stopPropagation();
            }
        }
    }

    return {
        add: function (elem, type, handler) {
            if (elem.setInterval && (elem !== window && !elem.frameElement)) {
                elem = window;
            }
            if (!handler.guid) {
                handler.guid = ++guid;
            }
            if (!elem.events) {
                elem.events = {};
                elem.handle = function (event) {
                    if (typeof Event !== "undefined") {
                        return commonHandle.call(elem, event);
                    }
                };
            }
            if (!elem.events[type]) {
                elem.events[type] = {};
                if (elem.addEventListener)
                    elem.addEventListener(type, elem.handle, false); else if (elem.attachEvent)
                    elem.attachEvent("on" + type, elem.handle);
            }
            elem.events[type][handler.guid] = handler;
        }, remove: function (elem, type, handler) {
            var handlers = elem.events && elem.events[type];
            if (!handlers)
                return;
            delete handlers[handler.guid];
            var any;
            for (any in handlers)
                return;
            if (elem.removeEventListener)
                elem.removeEventListener(type, elem.handle, false); else if (elem.detachEvent)
                elem.detachEvent("on" + type, elem.handle);
            delete elem.events[type];
            for (any in elem.events)
                return;
            try {
                delete elem.handle;
                delete elem.events;
            } catch (e) {
                elem.removeAttribute("handle");
                elem.removeAttribute("events");
            }
        }
    };
}());
function bindReady(handler) {
    var called = false;

    function ready() {
        if (called)
            return;
        called = true;
        handler()
    }

    if (document.addEventListener) {
        document.addEventListener("DOMContentLoaded", ready, false)
    } else if (document.attachEvent) {
        try {
            var isFrame = window.frameElement != null
        } catch (e) {
        }
        if (document.documentElement.doScroll && !isFrame) {
            function tryScroll() {
                if (called)
                    return;
                try {
                    document.documentElement.doScroll("left");
                    ready()
                } catch (e) {
                    setTimeout(tryScroll, 10)
                }
            }

            tryScroll()
        }
        document.attachEvent("onreadystatechange", function () {
            if (document.readyState === "complete") {
                ready()
            }
        })
    }
    if (window.addEventListener)
        window.addEventListener('load', ready, false);
    else if (window.attachEvent)
        window.attachEvent('onload', ready);
    else {
        var fn = window.onload;
        window.onload = function () {
            fn && fn();
            ready()
        }
    }
}
var readyList = [];
function onReady(handler) {
    function executeHandlers() {
        for (var i = 0; i < readyList.length; i++) {
            readyList[i]();
        }
    }

    if (!readyList.length) {
        bindReady(executeHandlers);
    }
    readyList.push(handler);
}
if (!String.prototype.trim) {
    String.prototype.trim = function () {
        return this.replace(/^\s+|\s+$/g, '');
    };
}
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};
function isLocalStorageAvailable() {
    try {
        return 'localStorage' in window && window['localStorage'] !== null;
    } catch (e) {
        return false;
    }
}
(function ($) {
    'use strict';
    var oldHover = $.fn.hover, newHover = function (handlerIn, handlerOut, delay) {
        return this.each(function () {
            var timeout, handler = function (el, fn, e) {
                if (timeout) {
                    timeout = window.clearTimeout(timeout);
                } else {
                    timeout = window.setTimeout(function () {
                        timeout = undefined;
                        fn.call(el, e);
                    }, delay);
                }
            };
            $(this).on('mouseenter mouseleave', function (e) {
                handler(this, e.type === 'mouseenter' ? handlerIn : handlerOut, e);
            });
        });
    };
    $.fn.hoverDelayed = function () {
        var args = Array.prototype.slice.call(arguments);
        if (args.length === 3 && typeof args[2] === 'number') {
            return newHover.apply(this, args);
        } else if (args.length === 2 && typeof args[1] === 'number') {
            return newHover.call(this, args[0], args[0], args[1]);
        }
        return oldHover.apply(this, args);
    };
})(window.jQuery);
function Rotation() {
    var self = this;
    self.elements = [];
    self.timerPosition = 1;
    self.init = function () {
        var elements = document.querySelectorAll('[data-rotation]');
        for (var i = 0; i < elements.length; i++) {
            var elem = elements[i];
            elem.classList.add('rotation');
            var config = self.parseConfig(elem.getAttribute('data-rotation'));
            if (config.target) {
                var targetElements = elem.querySelectorAll(config.target);
                self.initTargetElements(targetElements);
                elem.setAttribute('data-count', targetElements.length);
                elem.setAttribute('data-current', '1');
                if (config.interval) {
                    elem.setAttribute('data-trigger', '0');
                }
            }
            var navElement;
            if (config.nav) {
                navElement = elem.querySelector(config.nav);
            } else {
                navElement = elem;
            }
            var prevElement = navElement.querySelector('.prev');
            if (prevElement) {
                prevElement.addEventListener("click", self.clickPrev, false);
            }
            var nextElement = navElement.querySelector('.next');
            if (nextElement) {
                nextElement.addEventListener("click", self.clickNext, false);
            }
            if (config.pickerItems) {
                var pickerItems = elem.querySelectorAll(config.pickerItems);
                for (var p = 0; p < pickerItems.length; p++) {
                    var pickerItemNode = pickerItems[p];
                    if (pickerItemNode) {
                        pickerItemNode.addEventListener("click", self.pick, false);
                    }
                }
            }
            if (config.interval) {
                elem.setAttribute('data-interval', config.interval);
            }
            self.elements.push(elem);
            self.setVisibleByActive(elem);
        }
        self.initIntervals();
    };
    self.initTargetElements = function (targetElements) {
        for (var i = 0; i < targetElements.length; i++) {
            var elem = targetElements[i];
            if (i != 0) {
                elem.style.display = 'none';
                elem.style.opacity = 0;
            }
        }
    };
    self.initIntervals = function () {
        window.setInterval(function () {
            for (var i = 0; i < self.elements.length; i++) {
                var elem = self.elements[i];
                var trigger = elem.getAttribute('data-trigger') || 0;
                var interval = elem.getAttribute('data-interval') || 0;
                if (trigger == 0) {
                    if (interval > 0) {
                        if (self.timerPosition >= interval && self.timerPosition % interval == 0) {
                            self.next(elem);
                        }
                    }
                }
            }
            self.timerPosition++;
        }, 1000);
    };
    self.getRoot = function (element) {
        var parent = element.parentNode;
        if (parent) {
            if (nodeHasClass(parent, 'rotation')) {
                return parent;
            } else {
                return self.getRoot(parent);
            }
        }
        return false;
    };
    self.parseConfig = function (configString) {
        var config = {};
        $.each(configString.split(';'), function (index, value) {
            var keyVal = value.split(':');
            if (keyVal[0] && keyVal[1]) {
                config[keyVal[0].trim()] = keyVal[1].trim();
            }
        });
        return config;
    };
    self.clickPrev = function (e) {
        var rootNode = self.getRoot(e.target);
        self.triggerUp(rootNode);
        self.prev(rootNode);
    };
    self.clickNext = function (e) {
        var rootNode = self.getRoot(e.target);
        self.triggerUp(rootNode);
        self.next(rootNode);
    };
    self.pick = function (e) {
        var rootNode = self.getRoot(e.target);
        self.triggerUp(rootNode);
        var newPosition = e.target.getAttribute('data-pos');
        self.setPosition(newPosition, rootNode);
    };
    self.prev = function (rootNode) {
        var current = self.getCurrent(rootNode);
        var newPosition = (current === 1) ? self.getCount(rootNode) : current - 1;
        self.setPosition(newPosition, rootNode);
    };
    self.next = function (rootNode) {
        var current = self.getCurrent(rootNode);
        var newPosition = (current === self.getCount(rootNode)) ? 1 : current + 1;
        self.setPosition(newPosition, rootNode);
    };
    self.triggerUp = function (rootNode) {
        if (rootNode) {
            rootNode.setAttribute('data-trigger', '1');
        }
    };
    self.getCurrent = function (rootNode) {
        return parseInt(rootNode.getAttribute('data-current'));
    };
    self.getCurrentElement = function (rootNode) {
        var config = self.getConfig(rootNode);
        return rootNode.querySelector(config.nav + ' ' + config.current);
    };
    self.getTargetElements = function (rootNode) {
        var config = self.getConfig(rootNode);
        return rootNode.querySelectorAll(config.target);
    };
    self.getTargetRelElements = function (rootNode) {
        var config = self.getConfig(rootNode);
        return rootNode.querySelectorAll(config.targetRel);
    };
    self.getPickerElements = function (rootNode) {
        var config = self.getConfig(rootNode);
        return rootNode.querySelectorAll(config.pickerItems);
    };
    self.setTargetActive = function (newPosition, rootNode, targetElements, slide) {
        var i, animationSpeed = null;
        var config = self.getConfig(rootNode);
        if (config.animationSpeed) {
            animationSpeed = config.animationSpeed;
        }
        for (i = 0; i <= targetElements.length; i++) {
            var itemNode = targetElements[i];
            if ((newPosition - 1) === i) {
                if (itemNode) {
                    itemNode.classList.add('active');
                    if (slide === true) {
                        if (animationSpeed != null) {
                            $(itemNode).css('display', 'block').animate({opacity: 1}, animationSpeed);
                        } else {
                            itemNode.style.display = 'block';
                            itemNode.style.opacity = 1;
                        }
                    }
                }
            } else {
                if (itemNode) {
                    itemNode.classList.remove('active');
                    if (slide === true) {
                        if (animationSpeed != null) {
                            $(itemNode).css('display', 'none').animate({opacity: 0}, animationSpeed);
                        } else {
                            itemNode.style.display = 'none';
                            itemNode.style.opacity = 0;
                        }
                    }
                }
            }
        }
    };
    self.getCount = function (rootNode) {
        return parseInt(rootNode.getAttribute('data-count'));
    };
    self.getConfig = function (rootNode) {
        return self.parseConfig(rootNode.getAttribute('data-rotation'));
    };
    self.setPosition = function (newPosition, rootNode) {
        rootNode.setAttribute('data-current', newPosition);
        var currentElement = self.getCurrentElement(rootNode);
        if (currentElement) {
            currentElement.innerHTML = newPosition;
        }
        self.setTargetActive(newPosition, rootNode, self.getTargetElements(rootNode), true);
        self.setTargetActive(newPosition, rootNode, self.getTargetRelElements(rootNode), false);
        self.setTargetActive(newPosition, rootNode, self.getPickerElements(rootNode), false);
    };
    self.setVisibleByActive = function (element) {
        var activeItem = element.querySelector('.wrapper > .cluster > .item.active');
        if (activeItem) {
            var activeParent = activeItem.parentNode;
            var index = 0;
            while (activeParent = activeParent.previousSibling) {
                if (activeParent.nodeType === 1) {
                    ++index
                }
            }
            self.setPosition(index, element);
        }
    };
    return {init: self.init};
}
function nodeHasClass(el, clss) {
    return el.className && new RegExp("(^|\\s)" + clss + "(\\s|$)").test(el.className);
}
onReady(function () {
    var $menu = $('#menu');
    $menu.find('li').hoverDelayed(function () {
        $(this).addClass('hover');
    }, function () {
        $(this).removeClass('hover');
    }, 150);
    $menu.find("> li").hoverDelayed(function () {
        if ($(this).hasClass('parent')) {
            $(this).children('i').remove();
            var i = $("<i>").css('display', 'block');
            $(this).append(i);
        }
    }, function () {
        if (!$(this).hasClass('active')) {
            $(this).children('i').remove();
        }
    }, 150);
    $menu.find("> li.active.parent").each(function (index, element) {
        $(this).children('i').remove();
        var i = $("<i>").css('display', 'block');
        $(this).append(i);
    });
});
onReady(function () {
    var rotation = new Rotation();
    rotation.init();
    $('a.disabled').on('click', function (e) {
        e.preventDefault();
    });
});