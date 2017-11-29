var addSidebar, searchSidebar, settingsSidebar;
var addIcon, searchIcon, settingsIcon;


window.onload = function() {

    //prepare sidebars
    addSidebar = document.getElementById("sidebar-add");
    searchSidebar = document.getElementById("sidebar-search");
    settingsSidebar = document.getElementById("sidebar-settings");
    addIcon = document.getElementById("add-icon");
    searchIcon = document.getElementById("search-icon");
    settingsIcon = document.getElementById("settings-icon");
    addSidebar.style = "display: none"
    settingsSidebar.style = "display: none"

    //load all cards
    var json = JSON.stringify({
        action: "get-all"
    });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/', true)
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onreadystatechange = function() {
        if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {

            var response = JSON.parse(xhr.responseText);

            //set current db radiobutton
            document.getElementById("radio-memcached").checked = false;
            document.getElementById("radio-mongodb").checked = false;
            document.getElementById("radio-neo4j").checked = false;
            var radioButton = document.getElementById("radio-" + response.db);
            radioButton.checked = true;

            //add cards
            var cards = response.cards;
            var cardsHTML = ""
            for (var i = 0; i < cards.length; i++) {
                cardsHTML += getHTMLbyCard(cards[i]);
            }
            document.getElementById("cards").innerHTML = cardsHTML;

        } else {
            document.getElementById("cards").innerHTML = "<div style='width: 100%; text-align: center'>Ошибка подключения</div>";
        };
    }
    xhr.send(json);


}

function switchSidebar(sidebar) {
    if (sidebar == "add") {
        addIcon.src = "/img/active-add-icon.png";
        searchIcon.src = "/img/inactive-search-icon.png";
        settingsIcon.src = "/img/inactive-settings-icon.png";
        addSidebar.style = "display: block";
        searchSidebar.style = "display: none";
        settingsSidebar.style = "display: none";
    } 
    else if (sidebar == "search") {
        addIcon.src = "/img/inactive-add-icon.png";
        searchIcon.src = "/img/active-search-icon.png";
        settingsIcon.src = "/img/inactive-settings-icon.png";
        addSidebar.style = "display: none";
        searchSidebar.style = "display: block";
        settingsSidebar.style = "display: none";
    } 
    else if (sidebar == "settings") {
        addIcon.src = "/img/inactive-add-icon.png";
        searchIcon.src = "/img/inactive-search-icon.png";
        settingsIcon.src = "/img/active-settings-icon.png";
        addSidebar.style = "display: none";
        searchSidebar.style = "display: none";
        settingsSidebar.style = "display: block";
    }
}

function addCard() {
    var json = JSON.stringify({
        action: "add",
        title: document.getElementById("add-title").value,
        author: document.getElementById("add-author").value,
        year: document.getElementById("add-date").value,
        image: document.getElementById("add-image").value
    });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/', true)
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onreadystatechange = function() {
        if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (response.success == true) {
                document.getElementById("add-result").innerHTML = "Карточка добавлена";
                var card = {
                    id: response.id,
                    image: response.image,
                    title: response.title,
                    author: response.author,
                    year: response.year
                };
                document.getElementById("cards").innerHTML += getHTMLbyCard(card);
            } else {
                document.getElementById("add-result").innerHTML = "Ошибка при добавлении";
            }
        } else {
            document.getElementById("add-result").innerHTML = "Ошибка подключения";
        };
    }
    xhr.send(json);
}

function searchCards() {
    var json = JSON.stringify({
        action: "search",
        type: document.querySelector('input[name="search-type"]:checked').value,
        title: document.getElementById("search-title").value,
        author: document.getElementById("search-author").value,
        date: document.getElementById("search-date").value,
        id: document.getElementById("search-id").value
    });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/', true)
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onreadystatechange = function() {
        if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            cards = JSON.parse(xhr.responseText).cards;
            cardsHTML = ""
            for (var i = 0; i < cards.length; i++) {
                cardsHTML += getHTMLbyCard(cards[i]);
            }
            document.getElementById("cards").innerHTML = cardsHTML;
        } else {
            document.getElementById("search-result").innerHTML = "Ошибка подключения";
        };
    }
    xhr.send(json);
}

function switchDB() {
    var json = JSON.stringify({
        action: "switch-db",
        db: document.querySelector('input[name="db"]:checked').value
    });
    var xhr = new XMLHttpRequest();
    xhr.open("POST", '/', true)
    xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
    xhr.onreadystatechange = function() {
        if(this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            if (JSON.parse(xhr.responseText).success == true) {
                document.getElementById("apply-result").innerHTML = "База данных успешно изменена";
            } else {
                document.getElementById("apply-result").innerHTML = "Ошибка при изменеии базы данных";
            }
        } else {
            document.getElementById("apply-result").innerHTML = "Ошибка подключения";
        };
    }
    xhr.send(json);
}


function getHTMLbyCard(card) {
    var imageURL = card.image;
    if (imageURL == "null") imageURL = "";
    cardHTML = "";
    cardHTML += '<div id="' + card.id + '" class="card">';
    cardHTML += '<div class="card-image-container"><img class="card-image" src="' + imageURL + '"></img></div>';
    cardHTML += '<div class="card-info"><div class="card-info-item">';
    cardHTML += 'Название:<br><span class="field-value">' + card.title + '</span></div>';
    cardHTML += '<div class="card-info-item">Год выпуска:<br><span class="field-value">' + card.year + '</span></div>';
    cardHTML += '<div class="card-info-item">Автор:<br><span class="field-value">' + card.author + '</span></div>';
    cardHTML += '<div class="card-id">' + card.id + '</div></div></div>'
    return cardHTML;
}