var addSidebar, searchSidebar, settingsSidebar;
var addIcon, searchIcon, settingsIcon;


window.onload = function() {
    addSidebar = document.getElementById("sidebar-add");
    searchSidebar = document.getElementById("sidebar-search");
    settingsSidebar = document.getElementById("sidebar-settings");
    addIcon = document.getElementById("add-icon");
    searchIcon = document.getElementById("search-icon");
    settingsIcon = document.getElementById("settings-icon");
    addSidebar.style = "display: none"
    settingsSidebar.style = "display: none"
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