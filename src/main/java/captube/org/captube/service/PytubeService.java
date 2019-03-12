package captube.org.captube.service;

import captube.org.captube.custom.CaptubeImage;
import captube.org.captube.custom.CaptubeInfo;
import captube.org.captube.domain.CaptureItem;
import ch.qos.logback.core.util.FileUtil;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.ResourceLoader;
import org.springframework.stereotype.Service;

import javax.annotation.PostConstruct;
import java.io.*;
import java.util.*;
import java.util.concurrent.TimeUnit;

@Service
public class PytubeService {

    private Logger logger = LoggerFactory.getLogger(PytubeService.class);
    @Autowired
    private ResourceLoader resourceLoader;

    private static final String DEFAULT_LANGUAGE = "en";
    private static final String WORK_ROOT = System.getProperty("user.dir") + File.separator + "pytube";
    private static final String PYTUBE_SCRIPT_PATH = WORK_ROOT + File.separator + "get_youtube.py";
    private static final String CAPTURE_RESULT_PATH = WORK_ROOT + File.separator + "imgs";
    private static final String PREFIX_IMG = "downloaded_video";
    private static final int CAPTURE_TIMOUT = 15 * 60 * 1000;


    public CaptubeInfo getImages(String url, String fileName) throws Exception, IOException, InterruptedException {
        return getImages(url, DEFAULT_LANGUAGE, false, fileName);
    }

    public CaptubeInfo getImages
            (String url, String language, boolean isNosub, String fileName) throws Exception, IOException, InterruptedException {

        CaptubeInfo captubeInfo = new CaptubeInfo();
        ArrayList<CaptubeImage> images = new ArrayList<>();
        String title = "";

        logger.info("Start to run captube python script");

        Process captubeProcess = Runtime.getRuntime().exec(
                isNosub ?
                        new String[]{"python", PYTUBE_SCRIPT_PATH, "-u", url, "-l", language, "-n", fileName} :
                        new String[]{"python", PYTUBE_SCRIPT_PATH, "-u", url, "-l", language, "-n", fileName, "--no-sub"});
        captubeProcess.waitFor(CAPTURE_TIMOUT, TimeUnit.MILLISECONDS);
        logger.info("Running captube python script finished");

        if (captubeProcess.exitValue() == 0) {
            final BufferedReader reader = new BufferedReader(
                    new InputStreamReader(captubeProcess.getInputStream()));
            String line = null;
            while ((line = reader.readLine()) != null) {
                logger.info(line);
            }
            reader.close();

            String captubeJsonPath = WORK_ROOT + File.separator + fileName + ".json";
            File jsonFile = new File(captubeJsonPath);
            ObjectMapper mapper = new ObjectMapper();

            JsonNode resultJson = mapper.readTree(jsonFile);
            Iterator<JsonNode> frameInfos = resultJson.get("frame_infos").iterator();

            while(frameInfos.hasNext()){
                JsonNode frame = frameInfos.next();
                CaptubeImage captubeImage = new CaptubeImage();
                captubeImage.setImagePath(frame.get("img_path").asText());
                captubeImage.setStartTime(frame.get("time_info").asInt());
                captubeImage.setEndTime(frame.get("time_info").asInt());
                captubeImage.setScript(frame.get("script").asText());
                images.add(captubeImage);
            }

            title = resultJson.get("title").asText();
        } else {
            final BufferedReader reader = new BufferedReader(
                    new InputStreamReader(captubeProcess.getErrorStream()));
            String line = null;
            while ((line = reader.readLine()) != null) {
                logger.error(line);
            }
            reader.close();
            throw new Exception("Failed to capture youtube");
        }
        captubeInfo.setCaptubeImages(images.toArray(new CaptubeImage[images.size()]));
        captubeInfo.setTitle(title);

        return captubeInfo;
    }
}
