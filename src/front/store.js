export const initialStore = () => ({
  token: null,
  user: {},
  posts: [],
});

export default function storeReducer(store, action = {}) {
  if (action.type === "update_token") {
    return {
      ...store,
      token: action.token,
    };
  }

  if (action.type === "update_user") {
    return {
      ...store,
      user: action.user,
    };
  }

  if (action.type === "update_posts") {
    return {
      ...store,
      posts: action.posts,
    };
  }

  return store;
}
