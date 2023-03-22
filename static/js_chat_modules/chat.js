const chat_list_head = document.querySelector('.head')
function createDialog(data) {
    /*
    * data example::
    * data: {
    *   user: {
    *       'name': "John Doe",
    *       'user_id': 123
    *   },
    *   last-msg: {
    *       'author': "John Doe",
    *       'text': "Welcome to us"
    *   }
    * }
    * */
    let tem_div = document.createElement('div')
    let ava_div = document.createElement('div')
    let tex_div = document.createElement('div')
    let tit_div = document.createElement('div')
    let las_div = document.createElement('div')
    tem_div.classList.add('template')
    tem_div.setAttribute('data-peer-id', data['user']['user_id'])
    ava_div.classList.add('ava')
    tex_div.classList.add('text-box')
    tit_div.classList.add('title')
    tit_div.innerHTML = data['user']['name']
    las_div.classList.add('last-msg-text')
    las_div.setAttribute('data-author', data['last-msg']['author']+": ")
    las_div.innerHTML = data['last-msg']['text']
    tex_div.append(tit_div, las_div)
    tem_div.append(ava_div, tex_div)
    chat_list_head.after(tem_div)
    addCssEvents();
}
function addCssEvents() {
    let chats = document.querySelectorAll('.template')
    for (let _ of chats) {
        _.addEventListener('click', function () {
            let active = document.querySelector('.active_chat')
            if (active != null)
                active.classList.remove('active_chat')
            _.className = "active_chat " + _.className
        })
    }
}
function getCookie(name) {
    let ck = document.cookie;
    ck = ck.split('; ');
    for (let i = 0; i < ck.length; i++) {
        let pair = ck[i];
        let name = pair.split('=')[0];
        let value = pair.split('=')[1];
        ck[i] = {
            'name': name,
            'value' : value
        }
    }
    for (let pair of ck) {
        if (pair['name'] === name)
            return pair['value']
    }
    return null
}

addCssEvents();