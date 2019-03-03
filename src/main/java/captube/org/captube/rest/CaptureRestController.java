package captube.org.captube.rest;

import captube.org.captube.custom.CaptubeImage;
import captube.org.captube.domain.CaptureRequest;
import captube.org.captube.domain.CaptureResponse;
import captube.org.captube.service.PytubeService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.EnableAutoConfiguration;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.xml.ws.Response;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Base64;

import static captube.org.captube.common.Constants.EncodingType.BASE64;

@RestController
@RequestMapping("/api/v1/capture")
public class CaptureRestController {

    @Autowired
    private PytubeService pytubeService;

    @RequestMapping("/getImages")
    public ResponseEntity<CaptureResponse[]> getImages(@RequestBody  CaptureRequest request) {
        try {
            String url = request.getUrl();
            String responseEncodingType = request.getResponseEncodingType();
            String language = request.getLanguage();
            Boolean isNoSub = request.isNoSub();
            int numToCapture = request.getNumberToCapture();
            long startTime = request.getStartTimeStamp();
            long endTime = request.getEndTimeStamp();

            ArrayList<CaptureResponse> captureResponses = new ArrayList<>();
            CaptubeImage[] images = pytubeService.getImages(url);

            for (CaptubeImage image : images) {
                CaptureResponse reponseItem = new CaptureResponse();
                File captureFile = new File(image.getImagePath());

                FileInputStream inputStream = new FileInputStream(captureFile);
                ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();

                int len = 0;
                byte[] buf = new byte[1024];
                while ((len = inputStream.read(buf)) != -1) {
                    byteArrayOutputStream.write(buf, 0, len);
                }

                byte[] fileArray = byteArrayOutputStream.toByteArray();
                String fileString = null;

                if(responseEncodingType.equals(BASE64)){
                    fileString = new String(Base64.getEncoder().encode(fileArray));
                }
                else{
                    fileString = new String(fileArray);
                }

                reponseItem.setData(fileString);
                reponseItem.setFileName(captureFile.getName());
                reponseItem.setEncodingType(request.getResponseEncodingType());
                reponseItem.setStartTime(image.getStartTime());
                reponseItem.setEndTime(image.getEndTime());

                captureResponses.add(reponseItem);
            }
            ResponseEntity<CaptureResponse[]> response = new ResponseEntity<CaptureResponse[]>
                    (captureResponses.toArray(new CaptureResponse[captureResponses.size()]),HttpStatus.OK);

            return response;

        } catch (Exception e) {
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
