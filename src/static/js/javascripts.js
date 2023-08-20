function ChangeToMainA(){
    $("#main-box").fadeIn(200)
}
function ChangeToAccA(){
    $("#account-box").fadeIn(200)
}
function ChangeToSetA(){
    $("#setting-box").fadeIn(200)
}
function ChangeToMdlA(){
    $("#models-box").fadeIn(200)
}
function ChangeToWdgA(){
    $("#widgets-box").fadeIn(200)
}
function ChangeToRtsA(){
    $("#rights-box").fadeIn(200)
}

function ChangeToMain(){
    $("#login-box").fadeOut(1)
    $("#account-box").fadeOut(200)
    $("#models-box").fadeOut(200)
    $("#widgets-box").fadeOut(200)
    $("#setting-box").fadeOut(200)
    $("#rights-box").fadeOut(200)
    setTimeout(ChangeToMainA,250)
    $("#main").addClass("active")
    $("#acc").removeClass("active")
    $("#wig").removeClass("active")
    $("#mod").removeClass("active")
    $("#set").removeClass("active")
    $("#rts").removeClass("active")
}

function ChangeToAcc(){
    $("#login-box").fadeOut(1)
    $("#main-box").fadeOut(200)
    $("#models-box").fadeOut(200)
    $("#widgets-box").fadeOut(200)
    $("#setting-box").fadeOut(200)
    $("#rights-box").fadeOut(200)
    setTimeout(ChangeToAccA,250)
    $("#main").removeClass("active")
    $("#acc").addClass("active")
    $("#wig").removeClass("active")
    $("#mod").removeClass("active")
    $("#set").removeClass("active")
    $("#rts").removeClass("active")
}

function ChangeToSet(){
    $("#login-box").fadeOut(1)
    $("#main-box").fadeOut(200)
    $("#account-box").fadeOut(200)
    $("#models-box").fadeOut(200)
    $("#widgets-box").fadeOut(200)
    $("#rights-box").fadeOut(200)
    setTimeout(ChangeToSetA,250)
    $("#main").removeClass("active")
    $("#acc").removeClass("active")
    $("#wig").removeClass("active")
    $("#mod").removeClass("active")
    $("#set").addClass("active")
    $("#rts").removeClass("active")
}

function ChangeToMdl(){
    $("#login-box").fadeOut(1)
    $("#main-box").fadeOut(200)
    $("#account-box").fadeOut(200)
    $("#widgets-box").fadeOut(200)
    $("#setting-box").fadeOut(200)
    $("#rights-box").fadeOut(200)
    setTimeout(ChangeToMdlA,250)
    $("#main").removeClass("active")
    $("#acc").removeClass("active")
    $("#wig").removeClass("active")
    $("#mod").addClass("active")
    $("#set").removeClass("active")
    $("#rts").removeClass("active")
}

function ChangeToWdg(){
    $("#login-box").fadeOut(1)
    $("#main-box").fadeOut(200)
    $("#account-box").fadeOut(200)
    $("#models-box").fadeOut(200)
    $("#setting-box").fadeOut(200)
    $("#rights-box").fadeOut(200)
    setTimeout(ChangeToWdgA,250)
    $("#main").removeClass("active")
    $("#acc").removeClass("active")
    $("#wig").addClass("active")
    $("#mod").removeClass("active")
    $("#set").removeClass("active")
    $("#rts").removeClass("active")
}

function ChangeToRts(){
    $("#login-box").fadeOut(1)
    setTimeout(ChangeToRtsA,250)    
    $("#main").removeClass("active")
    $("#acc").removeClass("active")
    $("#wig").removeClass("active")
    $("#mod").removeClass("active")
    $("#set").removeClass("active")
    $("#rts").addClass("active")
}

function Loading(){
    $("#loading").fadeIn(100)
}
function Load() {
    $("#loading").fadeOut(100)
}

function show_widgets_edit(id) {
    $("#widgets_edit").fadeIn(100)
    var name = $("#widgets_"+id).attr("widgets_name")
    var url = $("#widgets_"+id).attr("widgets_url")
    $("#widgets_preview").attr("src", url)
    $("#widgets_name").val(name)
    $("#widgets_url").val(url)
}

//版本号
$(document).ready(function(){
    $("button").click(function(){
      $("#rights-box").fadeOut(100);
      $("#rts").removeClass("active")
    });
});

$(document).ready(function(){
    $("#widgets_close").click(function(){
      $("#widgets_edit").fadeOut(100);
    });
});

$(document).ready(function() {
//   拖动
var node = document.querySelector("#widgets_container")
	var draging = null
	node.ondragstart = function(event) {
		console.log("start:")
		// dataTransfer.setData把拖动对象的数据存入其中，可以用dataTransfer.getData来获取数据
		event.dataTransfer.setData("te", event.target.innerText)
		draging = event.target
	}
	node.ondragover = function(event) {
		console.log("over:")
		// 默认地，无法将数据/元素放置到其他元素中。如果需要设置允许放置，必须阻止对元素的默认处理方式
		event.preventDefault()
		var target = event.target
		if (target.nodeName === "LI" && target !== draging) {
			// 获取初始位置
			var targetRect = target.getBoundingClientRect()
			var dragingRect = draging.getBoundingClientRect()
			if (target) {
				// 判断是否动画元素
				if (target.animated) {
					return;
				}
			}
			if (_index(draging) < _index(target)) {
				// 目标比元素大，插到其后面
				// extSibling下一个兄弟元素
				target.parentNode.insertBefore(draging, target.nextSibling)
			} else {
				// 目标比元素小，插到其前面
				target.parentNode.insertBefore(draging, target)
			}
			_animate(dragingRect, draging)
			_animate(targetRect, target)
            load_active_widgets()
            upload_widgets_edit_order()
		}
	}

})

//Single
function change_tab(id){
    var now = $(".current").val()
    $(".current").removeClass("current")
    $("#Tab"+id).addClass("current")
    $('#'+now).fadeOut(100)
    $('#'+id).fadeIn(110)
}

//ajax Interface
//edit
function upload_widgets_edit_order(){
    var ctn = true
    var ele = document.getElementById("widgets_container")
    var child = ele.firstElementChild
    var last = ele.lastElementChild
    for (i =1;child != last + 1;i++){
        var value = child.id
        $.ajax({
            url: "/EditWidgetsOrder",
            method: "POST",
            data: {
                id: value,
                order: i,
            },
            success: function(response){
                if (response.response){
                    load_active_widgets()
                }
            }
        })
        child = child.nextElementSibling
    }
}

//prompt
function GetPrompts(id){
    var text = $("#user-input-"+id).val();
    var source_id = $("#user-input-"+id).attr("source_id");
    $.ajax({
        url: '/prompts',
        type: 'POST',
        data: {
            text: text,
        },
        success: function(prompts) {
            $('#Prompt-'+source_id).empty()
            e = 0
            for (i in prompts){
                $('#Prompt-'+source_id).append("\
                <button id='prompt-single-"+ e +"' class='prompt' value='"+ prompts[i] + "' source_id= " + id +" onclick='prompts(`" + e + "`)' >"+ i +"</button>")
                e++
            }
        }
    })
}
function prompts(id){
    var value = $("#prompt-single-"+id).val()
    var source_id = $("#prompt-single-"+id).attr("source_id");
    $('#Prompt-'+source_id).empty()
    $('#user-input-'+source_id).val(""+value)
}

function commit_model(id,operate){
    $("#loading").fadeIn(100)
    $('#'+operate+id).attr("disabled",true)
    $.ajax({
        url: '/exchange',
        type: 'POST',
        data: {
            state: operate ,
            number: $('#id'+id).val() ,
            comment: $('#Comment'+id).val() ,
            type: $('#Type'+id).val() ,
            url: $('#Url'+id).val() ,
            APIkey: $('#APIkey'+id).val() ,
            LcCompiler: $('#LcCompiler'+id).val() ,
            LcUrl: $('#LcUrl'+id).val() ,
        },
        success: function(response) {
            if (response.response){
                alert(response.message,"success")
                $("#loading").fadeOut(100)
                $('#'+operate+id).removeAttr("disabled")
            }
            else{
                alert(response.message,"danger")
                $("#loading").fadeOut(100)
                $('#'+operate+id).removeAttr("disabled")
            }
            Refresh_ModelList()
        }
    });
}

function SendInput(id) {
    if ($('#user-input-' + id).val() != ""){
        $("#loading").fadeIn(100);
        $('#output-' + id).append('<div class="item item-right"><div class="bubble bubble-right">' + $('#user-input-' + id).val() + '</div><div class="avatar"><i class="fa fa-user-circle"></i></div></div>');
        var input = $('#user-input-' + id).val()
        $('#user-input-' + id).val('');
        $.ajax({
            url: '/requestmodels',
            type: 'POST',
            data: {
                userinput: input,
                modelinput: $('#model-input-' + id).val(),
            },
            success: function(response) {
                var chatGptResponse = response.response;
                alert(chatGptResponse.message,"sucess")
                $('#output-' + id).append('<div class="item item-left"><div class="avatar"><i class="fa fa-user-circle-o"></i></div><div class="bubble bubble-left">' + chatGptResponse + '</div></div>');
                $("#loading").fadeOut(100)
                let height = document.querySelector('.content').scrollHeight;
                document.querySelector(".content").scrollTop = height;
            }
        });
    }
    else{
        alert('内容不能为空',"warning");
    }
}

$(document).ready(function() {
//send request
$("#add").on('click',function() {
    $("#loading").fadeIn(100)
    $('#add').attr("disabled",true)
    $.ajax({
        url: '/exchange',
        type: 'POST',
        data: {
            state: 'add' ,
            number: $('#id').val() ,
            type: $('#Type-1').val() ,
            comment: $('#Comment-1').val() ,
            url: $('#Url-1').val() ,
            APIkey: $('#APIkey-1').val() ,
            LcCompiler: $('#LcCompiler-1').val() ,
            LcUrl: $('#LcUrl-1').val() ,
        },
        success: function(response) {
            if (response.response){
                alert("添加成功","success")
                $("#loading").fadeOut(100)
                $('#add').removeAttr("disabled")
            }
            else{
                alert("添加失败","danger")
                $("#loading").fadeOut(100)
                $('#add').removeAttr("disabled")
            }
            $('#Comment-1').val("")
            $('#Url-1').val("")
            $('#APIkey-1').val("")
            $('#LcCompiler-1').val("")
            $('#LcUrl-1').val("")
            Refresh_ModelList()
        }
    });
});
})

$(document).ready(function() {
    $("#change-adjust").on("click",function(){
        var now = $("body").attr("class")
        if (now == "light"){
            $("body").removeClass("light")
            $("body").addClass("dark")
        }
        if (now == "dark"){
            $("body").removeClass("dark")
            $("body").addClass("light")
        }
    })
})

// Refresh Data
function refresh_website(){
    Refresh_ModelList();
    Refresh_Tabs();
    load_active_widgets();
    load_widgets();
    load_settings();
}

function setup_website(){
    Refresh_ModelList();
    Refresh_Tabs();
    load_active_widgets();
    load_widgets();
    load_settings();
}

function load_history(id) {
    $.ajax({
        url: "/GetHistory",
        method: "POST",
        data: {
            id: id,
        },
        success: function(data){
            $('#output-' + id).empty()
            for (i in data){
            $('#output-' + id).append('<div class="item item-right"><div class="bubble bubble-right">' + data[i].UserInput + '</div><div class="avatar"><i class="fa fa-user-circle"></i></div></div>');
            $('#output-' + id).append('<div class="item item-left"><div class="avatar"><i class="fa fa-user-circle-o"></i></div><div class="bubble bubble-left">' + data[i].response + '</div></div>');
            }
            let height = document.querySelector('.content').scrollHeight;
            document.querySelector(".content").scrollTop = height;
        }
    })
}

function Refresh_ModelList(){
    $.ajax({
        url: '/GetModelList',
        method: "POST",
        success: function(data){
            $('#ModelTable').empty()
            for (i in data){
                $('#ModelTable').append('<input type="hidden" id="id'+ data[i].id +'" value='+ data[i].id +'>')
                $('#ModelTable').append('\
                <tr id="ModelTr">\
                    <td>\
                    <select name="type" id="Type'+ data[i].id +'">\
                        <option>'+ data[i].type +'</option>\
                        <option>OpenAI</option>\
                        <option>WebUI</option>\
                        <option>API</option>\
                    </select>\
                    </td>\
                    <td> \
                        <input type="text" name="comment" id="Comment'+ data[i].id +'" placeholder="ChatGLM" value='+ data[i].name +'>\
                    </td>\
                    <td>\
                        <input type="text" class="url" id="Url'+ data[i].id +'" name="url" placeholder="127.0.0.1:8000" value='+ data[i].url +'>\
                    </td>\
                    <td>\
                        <input type="text" class="url" id="APIkey'+ data[i].id +'" name="APIkey" placeholder="sk-qwdjqfooajkash & none" value='+ data[i].api_key +'>\
                    </td>\
                    <td>\
                        <input type="text" class="url" id="LcCompiler'+ data[i].id +'" name="LcCompiler" placeholder=".\venv\python.exe & OpenAI" value='+ data[i].launch_compiler +'>\
                    </td>\
                    <td>\
                        <input type="text" class="url" id="LcUrl'+ data[i].id +'" name="LCurl" placeholder=".\ChatGLM\launch.py" value='+ data[i].launch_path +'>\
                    </td>\
                    <td>\
                        <button class="run" id="run-'+ data[i].id +'" value="'+ data[i].id +'" onclick="commit_model('+ data[i].id +',`run`)"><i class="fa fa-play"></i></button>\
                        <button class="stop" id="stop-'+ data[i].id +'" value="'+ data[i].id +'" onclick="commit_model('+ data[i].id +',`stop`)"><i class="fa fa-stop"></i></button>\
                    </td>\
                    <td>\
                        <button class="edit" id="edit-'+ data[i].id +'" value="'+ data[i].id +'" onclick="commit_model('+ data[i].id +',`edit`)"><i class="fa fa-edit"></i></button>\
                    </td>\
                    <td><button class="deny" id="del-'+ data[i].id +'" value="'+ data[i].id +'" onclick="commit_model('+ data[i].id +',`del`)"><i class="fa fa-trash"></i></button>\
                    </td>\
                </tr>')
                load_history(data[i].id)
            }
        }
    })
}


function Refresh_Tabs(){
    $.ajax({
        url: "/GetActiveModels",
        method: "POST",
        success(data){
            $("#tabs").empty()
            $("#Contents").empty()
            for (i in data){
                if (data[i].id == 1){
                $("#tabs").append('<li draggable="true" class="li current" id="Tab'+ data[i].id +'" value='+ data[i].id +' onclick="change_tab('+ data[i].id +')"><span>'+ data[i].name +'</span></li>')
                if (data[i].type == "OpenAI" || data[i].type == "API"){
                    $("#Contents").append('\
                    <div class="dialogbox_container" id='+ data[i].id +'>\
                        <div class="content" id="output-'+ data[i].id +'"></div>\
                        <div class="prompt_container" id="Prompt-'+ data[i].id +'">\
                        </div>\
                        <div class="input-area">\
                            </br>\
                            <div class="txtb">\
                                <textarea class="userInputArea" placeholder="输入内容" id="user-input-'+ data[i].id +'" source_id="'+ data[i].id +'" onInput="GetPrompts('+ data[i].id +')"></textarea>\
                            </div>\
                            <input id="model-input-'+ data[i].id +'" type="hidden" value='+ data[i].name +' />\
                            <div class="button-area">\
                                <button type="submit" id="SendInput" value="'+ data[i].id +'" onclick="SendInput(`'+ data[i].id +'`)">发 送</button>\
                            </div>\
                        </div>\
                    </div>')
                }
                if (data[i].type == "WebUI"){
                    $("#Contents").append('\
                    <div id='+ data[i].id +'">\
                        <iframe allow="autoplay *; encrypted-media *;" src="'+ data[i].url +'"></iframe>\
                    </div>')
                }
                }
                else{
                    $("#tabs").append('\
                    <li draggable="true" class="li" id="Tab'+ data[i].id +'" value='+ data[i].id +' onclick="change_tab('+ data[i].id +')"><span>'+ data[i].name +'</span></li>\
                    ')
                    if (data[i].type == "OpenAI" || data[i].type == "API"){
                        $("#Contents").append('\
                        <div class="dialogbox_container" id='+ data[i].id +' style="display: none;">\
                            <div class="content" id="output-'+ data[i].id +'"></div>\
                            <div class="prompt_container" id="Prompt-'+ data[i].id +'">\
                            </div>\
                            <div class="input-area">\
                                </br>\
                                <div class="txtb">\
                                    <textarea class="userInputArea" placeholder="输入内容" id="user-input-'+ data[i].id +'" source_id="'+ data[i].id +'" onInput="GetPrompts('+ data[i].id +')"></textarea>\
                                </div>\
                                <input id="model-input-'+ data[i].id +'" type="hidden" value='+ data[i].name +' />\
                                <div class="button-area">\
                                <button type="submit" id="SendInput" value="'+ data[i].id +'" onclick="SendInput(`'+ data[i].id +'`)">发 送</button>\
                                </div>\
                            </div>\
                        </div>')
                    }
                    if (data[i].type == "WebUI"){
                        $("#Contents").append('\
                        <div id='+ data[i].id +' style="display: none;" class="iframe_container">\
                            <iframe allow="autoplay *; encrypted-media *;" src="'+ data[i].url +'"></iframe>\
                        </div>')
                    }
                }
            }
            load_active_widgets()
        }
    })
}

function load_active_widgets(){
    $.ajax({
        url: "/GetActiveWidgets",
        method: "POST",
        success: function(data){
            $("#widgets_container_live").empty()
            for (i in data){
                $("#widgets_container_live").append('\
                <div class="widgets_contentbox">\
                    <iframe src='+ data[i].widgets_url +' frameborder=0></iframe>\
                </div>\
                ')
            }
        }
    })
}

function load_widgets(){
    $.ajax({
        url: "/GetWidgets",
        method: "POST",
        success: function(data){
            $("#widgets_container").empty()
            for (i in data){
                $("#widgets_container").append('\
                <li class="ele" draggable="true" id="'+ data[i].id +'" title="<iframe></iframe>">\
                    '+ data[i].widgets_name +' | \
                    '+ data[i].widgets_url +'\
                    <i class="fa fa-bars"></i>\
                    <i class="fa fa-info" id="widgets_'+ data[i].id +'" widgets_name="'+ data[i].widgets_name +'"\
                    widgets_url="'+ data[i].widgets_url +'" onclick="show_widgets_edit('+ data[i].id +')"></i>\
                </li>\
                ')
            }
        }
    })
}

function switch_load(id){
    var now_value = $("#"+id).val()
    if (now_value == "True"){
        $("#"+id).val("False")
    }
    if (now_value == "False"){
        $("#"+id).val("True")
    }
}

function save_settings(){
    $.ajax({
        url: "/EditSetting",
        method : "POST",
        data: {
            Theme : $("body").attr("class"),
            Language : $("#Language").val(),
            ActiveExamine : $("#ActiveExamine").val(),
            Timeout : $("#Timeout").val(),
            Host : $("#Host").val(),
            Port : $("#Port").val(),
            Develop : $("#Develop").val(),
        },
    success: function(data){
        if (data.response == true){
            alert("保存成功","success")
            alert("部分更改将在重启程序后生效","warning")
            load_settings()
        }
    }
    })
}

function load_settings(){
    $.ajax({
        url: "/GetSetting",
        method : "POST",
    success: function(data){
        if (data.response == "true"){
            var now = $("body").attr("class")
            if (now == data.Theme){}
            else{
                $("body").removeClass(now)
                $("body").addClass(data.Theme)
            }
            $("#"+data.Language).attr("selected",true)
            $("#ActiveExamine").val(data.ActiveExamine)
            if (data.ActiveExamine == "True"){
                $("#ActiveExamine_Checkbox").attr("checked",true)
            }
            else{
                $("#ActiveExamine_Checkbox").removeAttr("checked")
            }
            if (data.Develop == "True"){
                $("#Develop_Checkbox").attr("checked",true)
            }
            else{
                $("#Develop_Checkbox").removeAttr("checked")
            }
            $("#ActiveExamine").val(data.ActiveExamine)
            $("#Develop").val(data.Develop)
            $("#Timeout").val(data.Timeout)
            $("#Host").val(data.Host)
            $("#Port").val(data.Port)
            $("Develop").val(data.Develop)
        }
    }
    })
}

//CommitModel
function loading(){
    $("#loading").fadeIn(100)
    setTimeout(function(){ $("#loading").fadeOut(100) },1000)
}


// 获取元素在父元素中的index
function _index(el) {
    var index = 0
    if (!el || !el.parentNode) {
        return -1
    }
    // previousElementSibling：上一个兄弟元素
    while (el && (el = el.previousElementSibling)) {
        index++
    }
    return index
}
// 触发动画
function _animate(prevRect, target) {
    var ms = 300
    if (ms) {
        var currentRect = target.getBoundingClientRect()
        if (prevRect.nodeType === 1) {
            prevRect = prevRect.getBoundingClientRect()
        }
        _css(target, 'transition', 'none')
        _css(target, 'transform', 'translate3d(' +
            (prevRect.left - currentRect.left) + 'px,' +
            (prevRect.top - currentRect.top) + 'px,0)'
        );

        target.offsetWidth; // 触发重绘

        _css(target, 'transition', 'all ' + ms + 'ms');
        _css(target, 'transform', 'translate3d(0,0,0)');
        // 事件到了之后把transition和transform清空
        clearTimeout(target.animated);
        target.animated = setTimeout(function() {
            _css(target, 'transition', '');
            _css(target, 'transform', '');
            target.animated = false;
        }, ms);
    }
}

// 给元素添加style
function _css(el, prop, val) {
    var style = el && el.style
    if (style) {
        if (val === void 0) {
            if (document.defaultView && document.defaultView.getComputedStyle) {
                val = document.defaultView.getComputedStyle(el, '')
            } else if (el.currentStyle) {
                val = el.currentStyle
            }
            return prop === void 0 ? val : val[prop]
        } else {
            if (!(prop in style)) {
                prop = '-webkit-' + prop;
            }
            style[prop] = val + (typeof val === 'string' ? '' : 'px')
        }
    }
}