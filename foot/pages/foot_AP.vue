<template>
  <v-row justify="center">

    <v-col cols="8" style="font-size: 40px; text-align: left; font-weight: bold">
      <div style="padding-bottom: 20px"> Foot AP <span v-if="is_load"> [ loading... ] </span> </div>

      <v-row>
        <!--    이미지 입력    -->
        <v-col>
          <v-row>
            <v-col>
              <div style="width: 90%; margin: auto;">
                <div id="image-show" style="width: 100%; height: 200px; background: lightgray; margin-bottom: 10px;"></div>
                <v-row>
                  <v-col>
                    <input id="file-input" type="file" multiple v-show="false"/>
                    <div @click="onClickUpload" style="cursor: pointer; padding: 10px; background: lightgray; text-align: center; font-size: 14px; border-radius: 10px;"> Insert X-ray </div>
                  </v-col>

                  <v-col>
                    <div @click="analysis" style="cursor: pointer; padding: 10px; background: lightgray; text-align: center; font-size: 14px; border-radius: 10px;"> Analysis </div>
                  </v-col>
                </v-row>
              </div>
            </v-col>
          </v-row>
        </v-col>

        <!--    이미지 목록    -->
        <v-col>
          <v-row>
            <v-col>
              <div style="width: 90%; margin: auto; border: 1px solid lightgray">
                <div style="font-size: 20px; background: lightskyblue; padding: 5px;"> File List </div>
                <div style="width: 100%; height: 200px; overflow: scroll; font-size: 14px; padding: 5px;">
                  <div @click="showFile(item)" v-for="item in uploadFiles" :class="{active: item.name == cur_file.name}" style="cursor: pointer;"> {{ item["name"] }} </div>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row>

        <!--    모델링 이미지    -->
        <v-col>
          <div style="width: 90%; margin: auto;">
            <div style="font-size: 16px;"> A.I Analysis </div>

            <div v-show="!src_result" id="image-show" style="width: 100%; height: 200px; background: lightgray; margin-bottom: 10px; object-fit: contain"></div>
            <img v-show="src_result" :src="src_result" style="width: 100%; height: 250px; background: lightgray; object-fit: contain" alt="">

            <div @click="download_image" style="cursor: pointer; padding: 10px; background: lightgray; text-align: center; font-size: 14px; border-radius: 10px;"> Save to Image </div>
          </div>
        </v-col>

        <!--    모델링 결과   -->
        <v-col>
          <div style="width: 90%; height: 250px; margin: auto;">
            <div class="d-flex">
              <div @click="onTab('Hallux')" class="text-center" :class="tab === 'Hallux' ? 'active' : ''" style="width:50%; font-size: 16px; ">Hallux valgus</div>
              <div @click="onTab('Intermetatarsal')" class="text-center" :class="tab === 'Intermetatarsal' ? 'active' : ''" style="width:50%; font-size: 16px;">I-II Intermetatarsal</div>
            </div>

            <div v-show="!cur_tab_image" style="width: 100%; height: 200px; background: lightgray; margin-bottom: 10px; object-fit: contain"></div>
            <img v-show="cur_tab_image" :src="cur_tab_image" style="width: 100%; height: 200px; background: lightgray; object-fit: contain" alt="">

            <div style="font-size: 20px; margin-bottom: 20px;">{{ (result_csv.length > 0 && result_csv[0]["result"].length) > 0 ? result_csv[0]["result"][tab_index] : "-" }} degree</div>

            <div @click="download_zip" style="cursor: pointer; padding: 10px; background: lightgray; text-align: center; font-size: 14px; border-radius: 10px;"> Save to File </div>
          </div>
        </v-col>
      </v-row>
    </v-col>

  </v-row>
</template>

<script>
export default {
  name: 'IndexPage',
  layout: "MainLayout",
  data: ()  =>  ({
    is_load: false,
    tab: "Hallux",
    tab_index: 1,
    cur_tab_image: "",
    cur_file: "",
    src_result: "",
    src_hallux: "",
    src_inter: "",
  }),
  computed: {
    uploadFiles() {
      return this.$store.getters["app/get_files"]
    },
    result_csv() {
      return this.$store.getters["app/get_analysis_result"].filter(item => item.name == this.cur_file.name)
    }
  },
  methods: {
    onTab(tab) {
      this.tab = tab

      switch(tab) {
        case "Hallux": this.cur_tab_image = this.src_hallux; this.tab_index = 1; break
        case "Intermetatarsal": this.cur_tab_image = this.src_inter; this.tab_index = 2; break
      }
    },
    onClickUpload() {
      let myInput = document.getElementById("file-input");
      myInput.click();

      var store = this.$store

      myInput.addEventListener('change', function(e) {
        store.commit("app/set_files", this.files)
      });
    },
    showFile(file) {
      this.cur_file = file

      //새로운 이미지 div 추가
      var newImage = document.createElement("img");
      newImage.setAttribute("class", 'img');

      //이미지 source 가져오기
      newImage.src = URL.createObjectURL(file);

      newImage.style.width = "100%";
      newImage.style.height = "100%";
      // newImage.style.visibility = "hidden";   //버튼을 누르기 전까지는 이미지를 숨긴다
      newImage.style.objectFit = "contain";

      //이미지를 image-show div에 추가
      var container = document.getElementById('image-show');

      if(container.children.length > 0) {
        container.removeChild(container.children[0])
      }

      container.appendChild(newImage);

      // 이미지 출력
      this.onTab("Hallux")

      let file_name = this.cur_file.name

      let result_list = this.$store.getters["app/get_analysis_files"].filter(item => item.name == file_name)[0]["files"]

      if(result_list.length > 0) {
        this.src_result = result_list.filter(item => item.includes("result") && item.includes(file_name) && item.includes(".jpg"))[0]

        this.src_hallux = result_list.filter(item => item.includes("hv_") && item.includes(file_name) && item.includes(".jpg"))[0]
        this.src_inter = result_list.filter(item => item.includes("im_") && item.includes(file_name) && item.includes(".jpg"))[0]

        this.cur_tab_image = this.src_hallux

        this.src_download = this.$store.getters["app/get_zip_files"][0]["result"]
      }
    },
    async analysis() {
      // const date = new Date();
      // console.log(date); // Fri Jun 17 2022 11:27:28 GMT+0100 (British Summer Time)

      this.is_load = true

      await this.$axios.$get("/api/analysis/clear")
      await this.$store.commit("app/set_analysis_files", [])
      await this.$store.commit("app/set_analysis_result", [])
      await this.$store.commit("app/set_zip_file", [])

      for (let i = 0; i < this.uploadFiles.length; i++) {
        await this.$store.dispatch("app/analysis_ap", this.uploadFiles[i])
      }

      this.is_load = false

      // const date2 = new Date();
      // console.log(date2); // Fri Jun 17 2022 11:27:28 GMT+0100 (British Summer Time)

      let file_name = this.uploadFiles[0].name

      let result_list = this.$store.getters["app/get_analysis_files"].filter(item => item.name == file_name)[0]["files"]

      if(result_list.length > 0) {
        this.src_result = result_list.filter(item => item.includes("result") && item.includes(file_name) && item.includes(".jpg"))[0]

        this.src_hallux = result_list.filter(item => item.includes("hv_") && item.includes(file_name) && item.includes(".jpg"))[0]
        this.src_inter = result_list.filter(item => item.includes("im_") && item.includes(file_name) && item.includes(".jpg"))[0]

        this.showFile(this.uploadFiles[0])

        this.cur_tab_image = this.src_hallux

        this.src_download = this.$store.getters["app/get_zip_files"][0]["result"]
      }
    },
    download_image() {
      fetch(this.src_result)
          .then(response => response.blob())
          .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `result_${this.cur_file.name}.jpg`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          });
    },
    download_zip() {
      fetch(this.src_download)
          .then(response => response.blob())
          .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'result_ap.zip';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
          });
    }
  },
}
</script>

<style scoped>
.active { background: blue; color: white; }
</style>