export default {
  created () {
    const title = this.page_title
    if (title) {
      document.title = title
    }
  }
}