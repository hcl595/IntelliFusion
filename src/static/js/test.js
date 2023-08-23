const response = await fetch("http://127.0.0.1:5000/request_models_stream",{"userinput": "写一段c++的冒泡排序程序","modelinput": "gpt-3.5-turbo"});
const reader = response.body.getReader();

while (true) {
    const { value, done } = reader.read(); if (done) break;
}
console.log("Received", value);
console.log('Response fully received');