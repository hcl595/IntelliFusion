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

function showLogin(){
    $("#login-box").fadeIn(200)
}
function CloseLogin(){
    $("#login-box").fadeOut(200)
}

function toGLM() {
	document.getElementById("li_GLM").className="li current";
	document.getElementById("li_GPT").className="li";
	document.getElementById("li_SD").className="li";
	document.getElementById("li_WIG").className="li";
	$("#DefaultBox").fadeIn(100)
	$("#SecondBox").fadeOut(100)
	$("#ThridBox").fadeOut(100)
	$("#WidgtBox").fadeOut(100)
}
function toGPT() {
	document.getElementById("li_GLM").className="li";
	document.getElementById("li_GPT").className="li current";
	document.getElementById("li_SD").className="li";
	document.getElementById("li_WIG").className="li";
	$("#DefaultBox").fadeOut(100)
	$("#SecondBox").fadeIn(100)
	$("#ThridBox").fadeOut(100)
	$("#WidgtBox").fadeOut(100)
}
function toSD() {
	document.getElementById("li_GLM").className="li";
	document.getElementById("li_GPT").className="li";
	document.getElementById("li_SD").className="li current";
	document.getElementById("li_WIG").className="li";
	$("#DefaultBox").fadeOut(100)
	$("#SecondBox").fadeOut(100)
	$("#ThridBox").fadeIn(100)
	$("#WidgtBox").fadeOut(100)
}
function toWIG() {
	document.getElementById("li_GLM").className="li";
	document.getElementById("li_GPT").className="li";
	document.getElementById("li_SD").className="li";
	document.getElementById("li_WIG").className="li current";
	$("#DefaultBox").fadeOut(100)
	$("#SecondBox").fadeOut(100)
	$("#ThridBox").fadeOut(100)
	$("#WidgtBox").fadeIn(100)
}


function Loading(){
    $("#loading").fadeIn(100)
}
function Load() {
    $("#loading").fadeOut(100)
}

function TypeAnime(input){ //打字机动画
    var text = document.getElementById(input).getAttribute("data-text");//获取要输出的文字
    var index = 0;
    var element = document.getElementById(input);//获取元素
    function myprint() {
        if (index < text.length) {
            element.innerText = element.innerText + text.charAt(index);
            index++;
        } else {
            clearInterval(c);//输出完后关闭定时器
        }
    }
    var c = setInterval(myprint, 100);//定时器
}

//版本号
$(document).ready(function(){
    $("button").click(function(){
      $("#rights-box").fadeOut(100);
      $("#rts").removeClass("active")
    });
});


//Single
function change_tab(id){
    var now = $(".current").val()
    $(".current").removeClass("current")
    $("#Tab"+id).addClass("current")
    $('#'+now).fadeOut(100)
    $('#'+id).fadeIn(110)
}

//ajax Interface
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
            for (i in prompts){
                $('#Prompt-'+source_id).append("\
                <button id='prompt"+ source_id +"' class='prompt' value='"+ prompts[i] + "' source_id= " + source_id +' onclick="prompts('+ source_id +')" >'+ i +'</button>')
            }
        }
    })
}
function prompts(id){
    var value = $("#prompt"+id).val()
    var source_id = $("#prompt"+id).attr("source_id");
    $('#Prompt-'+source_id).empty()
    $('#user-input-'+id).val(""+value)
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

// function edit_settings()

// Refresh Data
function refresh_website(){
    Refresh_ModelList();
    Refresh_Tabs();
    load_active_widgets();
    load_widgets();
    load_settings();
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
                <div class="widgets_contentbox">\
                    <iframe src='+ data[i].widgets_url +' " frameborder=0></iframe>\
                </div>\
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
