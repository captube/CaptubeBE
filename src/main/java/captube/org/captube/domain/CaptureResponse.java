package captube.org.captube.domain;

public class CaptureResponse {
    private String title;
    private CaptureItem[] captureItems;

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public CaptureItem[] getCaptureItems() {
        return captureItems;
    }

    public void setCaptureItems(CaptureItem[] captureItems) {
        this.captureItems = captureItems;
    }
}
