package captube.org.captube.rest;

import captube.org.captube.custom.CaptubeImage;
import captube.org.captube.custom.CaptubeInfo;
import captube.org.captube.domain.CaptureRequest;
import captube.org.captube.domain.CaptureItem;
import captube.org.captube.domain.CaptureResponse;
import captube.org.captube.service.PytubeService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.Base64;
import java.util.UUID;

import static captube.org.captube.common.Constants.EncodingType.BASE64;

@RestController
@RequestMapping("/api/v1/capture")
public class CaptureRestController {

    private Logger logger = LoggerFactory.getLogger(CaptureRestController.class);

    @Autowired
    private PytubeService pytubeService;

    @RequestMapping("/getImages")
    public ResponseEntity<CaptureResponse> getImages(@RequestHeader(value = "Origin") String origin, @RequestBody CaptureRequest request) {
        try {
            String url = request.getUrl();
            String responseEncodingType = request.getResponseEncodingType();
            String language = request.getLanguage();
            Boolean isNoSub = request.isNoSub();
            int numToCapture = request.getNumberToCapture();
            long startTime = request.getStartTimeStamp();
            long endTime = request.getEndTimeStamp();

            ArrayList<CaptureItem> captureItems = new ArrayList<>();
            logger.info("Start to get capture images from service");
            logger.info("Generating unique id for request");
            String id = UUID.randomUUID().toString().replace("-", "");
            logger.info("Generate unique id : {}", id);
            CaptubeInfo info = pytubeService.getImages(url, language, isNoSub, id);
            CaptubeImage[] images = info.getCaptubeImages();

            for (CaptubeImage image : images) {
                logger.info("Generating response for image {}", image.getImagePath());
                CaptureItem reponseItem = new CaptureItem();
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

                logger.info("Encoding image data in {} for image {}", responseEncodingType, image.getImagePath());
                if (responseEncodingType.equals(BASE64)) {
                    fileString = new String(Base64.getEncoder().encode(fileArray));
                } else {
                    fileString = new String(fileArray);
                }

                reponseItem.setData(fileString);
                reponseItem.setScript(image.getScript());
                reponseItem.setFileName(captureFile.getName());
                reponseItem.setEncodingType(request.getResponseEncodingType());
                reponseItem.setStartTime(image.getStartTime());
                reponseItem.setEndTime(image.getEndTime());

                captureItems.add(reponseItem);
            }


            CaptureResponse captureResponse = new CaptureResponse();
            captureResponse.setTitle(info.getTitle());
            captureResponse.setCaptureItems(captureItems.toArray(new CaptureItem[captureItems.size()]));

            ResponseEntity<CaptureResponse> response = new ResponseEntity<CaptureResponse>
                    (captureResponse, HttpStatus.OK);

            logger.info("Response for image capture");
            return response;

        } catch (Exception e) {
            e.printStackTrace();
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
}
