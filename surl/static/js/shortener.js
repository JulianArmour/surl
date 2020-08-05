const urlInput = document.getElementById("url-input")
const shortenBtn = document.getElementById("shorten-btn");
const customInput = document.getElementById("custom-input");
const errorTxt = document.getElementById("error-text")

function requestShortened(data, callback, error) {
    const r = new XMLHttpRequest();
    r.onreadystatechange = function () {
        if (this.readyState === 4) {
            if (this.status === 200) {
                callback(JSON.parse(this.responseText));
            } else {
                error(this.status, JSON.parse(this.responseText));
            }
        }
    }
    r.open("POST", "/api/urls", true);
    r.setRequestHeader("Content-type", "application/json");
    r.send(JSON.stringify(data));
}

function App() {
    this.state = new Shortening();

    this.handleButtonClick = function () {
        this.state.handleButtonClick(this);
    }
}

function Shortening() {
    shortenBtn.textContent = "Shorten";
    urlInput.removeAttribute("readonly");

    this.handleButtonClick = function (app) {
        const data = {original_url: urlInput.value};
        const customStr = customInput.value;
        if (customStr) {
            data.short_str = customStr;
        }

        requestShortened(data,
            (data) => {
                app.state = new Copying(data["_links"]["short_url"]["href"]);
            },
            (statusCode, errorMsg) => {
                if (statusCode === 409) {
                    errorTxt.textContent = errorMsg;
                }
            }
        );
    };
}

function Copying(url) {
    shortenBtn.textContent = "Copy";
    urlInput.value = url;
    urlInput.setAttribute("readonly", "");
    urlInput.select();
    errorTxt.textContent = "";

    this.handleButtonClick = function (app) {
        urlInput.select();
        urlInput.setSelectionRange(0, 99999);
        document.execCommand("copy");
        app.state = new Shortening();
    }
}

const app = new App();