<template>
  <v-row>
    <v-col>
      <v-card rounded="0">
        <v-toolbar>
          <v-card-title class="flex-fill px-0">
            <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="회원검색"
                single-line
                hide-details
            ></v-text-field>
          </v-card-title>

          <v-spacer/>

          <v-btn @click="open_form" color="secondary" dark>
            회원등록
          </v-btn>
        </v-toolbar>

          <v-data-table
              :headers="headers"
              :items="user_list"
              :search="search"
          >

          <template v-slot:item.actions="{ item }">
            <v-icon small @click="delete_item(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card>
    </v-col>

    <v-dialog max-width="600px" :fullscreen="$vuetify.breakpoint.xsOnly" v-model="is_open_user_form">
      <user-form :is_open_user_form="is_open_user_form" @close_modal="is_open_user_form = false" />
    </v-dialog>
  </v-row>
</template>

<script>
export default {
  name: 'AdminLoginPage',
  layout: "AdminLayout",
  data: ()  =>  ({
    search: '',
    headers: [
      { text: '회원 아이디', value: 'uid' },
      { text: '회원 이름', value: 'name' },
      { text: '회원 이메일', value: 'email' },
      { text: '회원 연락처', value: 'phone'  },
      { text: '가입일', value: 'regist_dt' },
      { text: '삭제', value: 'actions' },
    ],
    is_open_user_form: false,
  }),
  computed: {
    user_list() {
      return this.$store.getters["app/get_user_list"] || []
    },
  },
  created() {
    this.$store.dispatch("app/fetch_user_list")
  },
  methods: {
    open_form() {
      this.$store.commit('app/set_selected_user', null)
      this.is_open_user_form = true
    },
    edit_item(user) {
      this.$store.commit('app/set_selected_user', user)
      this.is_open_user_form = true
    },
    async delete_item(user) {
      if(confirm("사용자를 삭제하시겠습니까?")) {
        await this.$store.dispatch("app/delete_user", user)
        await this.$store.dispatch("app/fetch_user_list")
      }
    },
  }
}
</script>