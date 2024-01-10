const state = () => ({
  user: null,
  uploadFiles: [],
  analysis_files: [],
  analysis_result: [],
  zip_files: [],
  user_list: [],
});

const getters = {
  get_user: (state) => state.user,
  get_files: (state) => state.uploadFiles,
  get_zip_files: (state) => state.zip_files,
  get_analysis_files: (state) => state.analysis_files,
  get_analysis_result: (state) => state.analysis_result,
  get_user_list: (state) => state.user_list,
};

const mutations = {
  set_user(state, payload) {
    state.user = payload
  },
  set_files(state, payload) {
    state.uploadFiles = payload
  },
  set_analysis_files(state, payload) {
    state.analysis_files = payload
  },
  set_analysis_result(state, payload) {
    state.analysis_result = payload
  },
  set_zip_file(state, payload) {
    state.zip_files = payload
  },
  set_user_list(state, payload) {
    state.user_list = payload
  },
};

const actions = {
  async login(context, payload) {
    let params = {
      id: payload.id,
      password: payload.password,
    }

    let res = await this.$axios.$post("/api/users/login", params)

    if(res["is_login"] === false) {
      alert(res["message"])
    } else {
      context.commit('set_user', res["user"]);
    }
  },
  async admin_login(context, payload) {
    let params = {
      id: payload.id,
      password: payload.password,
    }

    let res = await this.$axios.$post("/api/admin/users/login", params)

    if(res["is_login"] === false) {
      alert(res["message"])
    } else {
      context.commit('set_user', res["user"]);
    }
  },
  async analysis_lateral(context, payload) {
    const form = new FormData()
    form.append('file', payload)

    let res = await this.$axios.$post("/api/analysis/lateral", form, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
    })

    console.log(payload.name)
    console.log(res["result_csv"])

    let files = Array.from(context.state.analysis_files)
    files.push({ name: payload.name, files: res["result"] })
    context.commit('set_analysis_files', files);

    let result = Array.from(context.state.analysis_result)
    res["result_csv"].map(item => {
      if(item.includes(payload.name)) {
        result.push({ name: payload.name, result: item })
      }
    })
    context.commit('set_analysis_result', result);

    let zip = Array.from(context.state.zip_files)
    zip.push({ name: payload.name, result: res["zip_src"] })
    context.commit("set_zip_file", zip)
  },
  async analysis_ap(context, payload) {
    const form = new FormData()
    form.append('file', payload)

    let res = await this.$axios.$post("/api/analysis/ap", form, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
    })

    let files = Array.from(context.state.analysis_files)
    files.push({ name: payload.name, files: res["result"] })
    context.commit('set_analysis_files', files);

    let result = Array.from(context.state.analysis_result)
    res["result_csv"].map(item => {
      if(item.includes(payload.name)) {
        result.push({ name: payload.name, result: item })
      }
    })
    context.commit('set_analysis_result', result);

    let zip = Array.from(context.state.zip_files)
    zip.push({ name: payload.name, result: res["zip_src"] })
    context.commit("set_zip_file", zip)
  },
  async fetch_user_list(context, payload) {
    let res = await this.$axios.$get("/api/admin/users")

    context.commit("set_user_list", res["items"])
  },
  async regist_user(context, payload) {
    let res = await this.$axios.$post(`/api/admin/users`, payload)

    if (res.msg) {
      alert(res.msg)
    }
  },
  async delete_user(context, payload) {
    let params = { uid: payload.uid }
    let res = await this.$axios.$delete(`/api/admin/users/${params.uid}`)

    if (res.msg) {
      alert(res.msg)
    }
  },
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions,
};
