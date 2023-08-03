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

function msgshow(choose){ //Toast显示错误
    if (choose == 1)
    showToast('{{ error }}',800);
}

function showToast(msg,duration){ //Toast弹窗
    duration=isNaN(duration)?3000:duration;
    var m = document.createElement('div');
    m.innerHTML = msg;
    m.style.cssText="width:100px; min-width:180px; background:#000; opacity:0.6; height:auto;min-height: 30px; color:#fff; line-height:30px; text-align:center; border-radius:4px; position:fixed; top:50%; left:45.5%; z-index:999999;";
    document.body.appendChild(m);
    setTimeout(function() {
        var d = 0.5;
        m.style = '-webkit-transform ' + d + 's ease-in, opacity ' + d + 's ease-in';
        m.style.opacity = '0';
        setTimeout(function() { document.body.removeChild(m) }, d * 10);
    }, duration);
}

function edit_msg(edit_judge_msg){ //Toast弹窗一体化
if (edit_judge_msg == 1)
    showToast('{{ edit_msg }}',800);
    let height = document.querySelector('.content').scrollHeight;
    document.querySelector(".content").scrollTop = height;
}
function checkbox(check_id,check_judge){
if (check_judge == 1)
    document.getElementById(check_id).checked = True
if (check_judge == 0)
    document.getElementById(check_id).checked = False
}

//版本号


$(document).ready(function(){
    $("button").click(function(){
      $("#rights-box").fadeOut(100);
      $("#rts").removeClass("active")
    });
});
//单个组件


