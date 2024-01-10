<template>
  <v-row justify="center">

    <v-col cols="6">
      <v-row>
        <v-col>
          <div @click="onTab('Lateral')" class="text-center" :class="tab === 'Lateral' ? 'active' : ''" style="padding: 10px; cursor: pointer;">
            Foot Lateral
          </div>
        </v-col>

        <v-col>
          <div @click="onTab('AP')" class="text-center" :class="tab === 'AP' ? 'active' : ''" style="padding: 10px; cursor: pointer;">
            Foot AP
          </div>
        </v-col>
      </v-row>
    </v-col>

    <v-col class="mb-5 mt-5" cols="12" align="center">
      <div @click="moveTo('Lateral')" v-show="tab === 'Lateral'" class="text-center" style="width: 200px; padding: 10px; border-radius: 10px; background: #bdbdbd; ; cursor: pointer;">
        Prediction
      </div>
      <div @click="moveTo('AP')" v-show="tab === 'AP'" class="text-center" style="width: 200px; padding: 10px; border-radius: 10px; background: #bdbdbd; ; cursor: pointer;">
        Prediction
      </div>
    </v-col>

    <!--  Foot Lateral  -->
    <div v-show="tab === 'Lateral'">
      <v-col cols="12">
        <v-row justify="center" align="center">
          <v-col cols="4">
            <img src="@/static/lateral_origin.jpg" alt="" width="100%">
          </v-col>

          <v-col cols="2" style="padding: 20px">
            <img src="@/static/arrow.png" alt="" width="100%">
          </v-col>

          <v-col cols="4">
            <img src="@/static/lateral_keypoints.jpg" alt="" width="100%">
          </v-col>
        </v-row>
      </v-col>

      <v-col class="mb-5" cols="12">
      <v-row justify="center">
        <v-col cols="8" style="font-size: 20px">
          - Description <br>
          In the Foot Lateral X-ray radiograph, AI predicts and measures 5 types of angles: <br>
          Calcaneal pitch(sesamoid), Calcaneal pitch(5th metatarsal), Boehler angle, Meary’s <br>
          angle, Talar declination angle <br>
          * The higher the positive value of Meary's angle, the closer it is to flat foot (pes planus). <br>
          * The more negative the Meary's angle, the closer it is to pes cavus. <br>
        </v-col>
      </v-row>
    </v-col>
    </div>

    <!--  Foot AP  -->
    <div v-show="tab === 'AP'">
      <v-col cols="12">
        <v-row justify="center" align="center">
          <v-col cols="4">
            <img src="@/static/ap_origin.jpg" alt="" width="100%">
          </v-col>

          <v-col cols="2" style="padding: 20px">
            <img src="@/static/arrow.png" alt="" width="100%">
          </v-col>

          <v-col cols="4">
            <img src="@/static/ap_keypoints.jpg" alt="" width="100%">
          </v-col>
        </v-row>
      </v-col>

      <v-col class="mb-5" cols="12">
        <v-row justify="center">
          <v-col cols="8" style="font-size: 20px">
            - Description <br>
            In the Foot AP X-ray radiograph, AI predicts and measures 2 types of angles: <br>
            Hallux valgus angle, 1st-2nd intermetatarsal angle <br>
          </v-col>
        </v-row>
      </v-col>
    </div>

  </v-row>
</template>

<script>
export default {
  name: 'MainPage',
  layout: "MainLayout",
  data: ()  =>  ({
    form: {
      user_id: "",
      password: "",
    },
    tab: "Lateral"
  }),
  mounted() {
    this.$store.commit("app/set_files", [])
  },
  methods: {
    onTab(tab) {
      this.tab = tab
    },
    moveTo(path) {
      switch(path) {
        case "Lateral": this.$router.push("foot_lateral"); break
        case "AP": this.$router.push("foot_AP"); break
      }
    }
  }
}
</script>

<style scoped>
.active { border-bottom: 2px solid blue; }
</style>
