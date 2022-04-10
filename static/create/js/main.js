
// var myModal = document.getElementById('myModal')
// var myInput = document.getElementById('myInput')
//
// myModal.addEventListener('shown.bs.modal', function () {
//   myInput.focus()
// })



var background_layer = document.getElementsByClassName('Background')[0];
var rare_background_layer = document.getElementsByClassName('Rare Background')[0];
var member_layer = document.getElementsByClassName('Member')[0];
var pants_layer = document.getElementsByClassName('Pants')[0];
var clothes_layer = document.getElementsByClassName('Clothes')[0];
var expresion_layer = document.getElementsByClassName('Expresion')[0];
var vr_layer = document.getElementsByClassName('Headset')[0];
var hair_layer = document.getElementsByClassName('Hair')[0];
var head_layer = document.getElementsByClassName('Head')[0];


var background_form = document.getElementsByClassName('background_form')[0];
var rare_background_form = document.getElementsByClassName('rare_background_form')[0];
var member_form = document.getElementsByClassName('member_form')[0];
var pants_form = document.getElementsByClassName('pants_form')[0];
var clothes_form = document.getElementsByClassName('clothes_form')[0];
var expresion_form = document.getElementsByClassName('expresion_form')[0];
var vr_form = document.getElementsByClassName('vr_form')[0];
var hair_form = document.getElementsByClassName('hair_form')[0];
var head_form = document.getElementsByClassName('head_form')[0];


var count_images = document.getElementById('count_images');
var layer_name = document.getElementById('layer-name');



background_form.addEventListener('change', function(event) {
    length = background_form.files.length;
    count_images.textContent = length;
})

rare_background_form.addEventListener('change', function(event) {
    length = rare_background_form.files.length;
    count_images.textContent = length;
})

member_form.addEventListener('change', function(event) {
    length = member_form.files.length;
    count_images.textContent = length;
})

pants_form.addEventListener('change', function(event) {
    length = pants_form.files.length;
    count_images.textContent = length;
})

clothes_form.addEventListener('change', function(event) {
    length = clothes_form.files.length;
    count_images.textContent = length;
})

expresion_form.addEventListener('change', function(event) {
    length = expresion_form.files.length;
    count_images.textContent = length;
})

vr_form.addEventListener('change', function(event) {
    length = vr_form.files.length;
    count_images.textContent = length;
})

hair_form.addEventListener('change', function(event) {
    length = hair_form.files.length;
    count_images.textContent = length;
})

head_form.addEventListener('change', function(event) {
    length = head_form.files.length;
    count_images.textContent = length;
})




background_form.name = 'background_form';
rare_background_form.name = 'rare_background_form';
member_form.name = 'member_form';
pants_form.name = 'pants_form';
clothes_form.name = 'clothes_form';
expresion_form.name = 'expresion_form';
vr_form.name = 'vr_form';
hair_form.name = 'hair_form';
head_form.name = 'head_form';


background_layer.style.border = '1px solid #fff';
rare_background_form.style.display = 'none';
member_form.style.display = 'none';
pants_form.style.display = 'none';
clothes_form.style.display = 'none';
expresion_form.style.display = 'none';
vr_form.style.display = 'none';
hair_form.style.display = 'none';
head_form.style.display = 'none';


background_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Background'
    background_layer.style.border = '1px solid #fff';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';


    background_form.style.display = 'block';
    rare_background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';
})

rare_background_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Rare';
    background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';

    rare_background_layer.style.border = '1px solid #fff';
    rare_background_form.style.display = 'block';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';

})

member_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Member'
    member_layer.style.border = '1px solid #fff';
    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';


    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'block';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';
})

pants_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Pants'
    pants_layer.style.border = '1px solid #fff';

    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';

    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'block';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';
})

clothes_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Clothes'
    clothes_layer.style.border = '1px solid #fff';

    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';

    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'block';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';
})

expresion_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Expresion'
    expresion_layer.style.border = '1px solid #fff';

    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';

    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'block';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';
})

vr_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Headset'
    vr_layer.style.border = '1px solid #fff';

    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    hair_layer.style.border = '0';
    head_layer.style.border = '0';

    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'block';
    hair_form.style.display = 'none';
    head_form.style.display = 'none';
})

hair_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Hair'
    hair_layer.style.border = '1px solid #fff';

    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    head_layer.style.border = '0';

    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'block';
    head_form.style.display = 'none';
})

head_layer.addEventListener('click', function (e) {
    layer_name.textContent = 'Head'
    head_layer.style.border = '1px solid #fff';

    background_layer.style.border = '0';
    rare_background_layer.style.border = '0';
    member_layer.style.border = '0';
    pants_layer.style.border = '0';
    clothes_layer.style.border = '0';
    expresion_layer.style.border = '0';
    vr_layer.style.border = '0';
    hair_layer.style.border = '0';

    rare_background_form.style.display = 'none';
    background_form.style.display = 'none';
    member_form.style.display = 'none';
    pants_form.style.display = 'none';
    clothes_form.style.display = 'none';
    expresion_form.style.display = 'none';
    vr_form.style.display = 'none';
    hair_form.style.display = 'none';
    head_form.style.display = 'block';
})

