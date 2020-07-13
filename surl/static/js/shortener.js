function requestShortened(long_url, callback) {
    const r = new XMLHttpRequest();
    r.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callback(JSON.parse(this.responseText));
        }
    }
    r.open("POST", "/api/urls", true);
    r.setRequestHeader("Content-type", "application/json");
    const data = JSON.stringify({
        original_url: long_url,
    });
    r.send(data);
}

function App() {
    this.state = new Shortening();

    this.handleButtonClick = function () {
        this.state.handleButtonClick(this);
    }
}

function Shortening() {
    this.urlInput = document.getElementById("url-input")
    this.button = document.getElementById("shorten-btn");

    this.button.textContent = "Shorten";
    this.urlInput.removeAttribute("readonly")

    this.handleButtonClick = function (app) {
        requestShortened(this.urlInput.value, (data) => {
            app.state = new Copying(data["_links"]["short_url"]["href"]);
        });
    };
}

function Copying(url) {
    this.urlInput = document.getElementById("url-input")
    this.button = document.getElementById("shorten-btn");

    this.button.textContent= "Copy";
    this.urlInput.value = url;
    this.urlInput.setAttribute("readonly", "");
    this.urlInput.select();

    this.handleButtonClick = function (app) {
        this.urlInput.select();
        this.urlInput.setSelectionRange(0, 99999);
        document.execCommand("copy");
        app.state = new Shortening();
    }
}

const app = new App();