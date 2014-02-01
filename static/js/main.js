function getTime(string) {
    // times by 1000 as JS uses milliseconds and i store seconds
    var date = new Date(string * 1000);
    return date.toUTCString();
}
