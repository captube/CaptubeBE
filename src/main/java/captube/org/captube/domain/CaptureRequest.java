package captube.org.captube.domain;

public class CaptureRequest {
    private String url;
    private String language;
    private String responseEncodingType;
    private boolean isNoSub;
    private int numberToCapture;
    private long startTimeStamp;
    private long endTimeStamp;

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getResponseEncodingType() {
        return responseEncodingType;
    }

    public void setResponseEncodingType(String responseEncodingType) {
        this.responseEncodingType = responseEncodingType;
    }

    public int getNumberToCapture() {
        return numberToCapture;
    }

    public void setNumberToCapture(int numberToCapture) {
        this.numberToCapture = numberToCapture;
    }

    public long getStartTimeStamp() {
        return startTimeStamp;
    }

    public void setStartTimeStamp(long startTimeStamp) {
        this.startTimeStamp = startTimeStamp;
    }

    public long getEndTimeStamp() {
        return endTimeStamp;
    }

    public void setEndTimeStamp(long endTimeStamp) {
        this.endTimeStamp = endTimeStamp;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public boolean isNoSub() {
        return isNoSub;
    }

    public void setNoSub(boolean noSub) {
        isNoSub = noSub;
    }
}
