import axios from "axios";
import { useNavigate } from "react-router-dom";
import axiosService from "../helpers/axios";

function useUserActions() {
  const navigate = useNavigate();
  const baseURL = "http://localhost:8000/api/v1";

  return {
    login,
    register,
    logout,
    edit,
  };

  function edit(data, userId) {
    return axiosService.patch(`${baseURL}/user/${userId}/`,
    data, { headers: {
      'Content-Type': "mutipart/form-data"
    } }).then((res) => {
    const  { username, first_name, last_name, email, id, avatar } = res.data;
    const user_data = { username, first_name, last_name, email, id, avatar };
    localStorage.setItem(
    "auth",
    JSON.stringify({
    access: getAccessToken(),
    refresh: getRefreshToken(),
    user: user_data,
    })
    );
    });
    }


  function login(data) {
    return axios.post(`${baseURL}/auth/login/`, data).then((res) => {
      
      setUserData(res.data);
      navigate("/");
    });
  }

 
  function register(data) {
    return axios.post(`${baseURL}/auth/register/`, data).then((res) => {
     
      setUserData(res.data);
      navigate("/");
    });
  }

  
  function logout() {
    localStorage.removeItem("auth");
    navigate("/login");
  }
}


function getUser() {
  const auth = JSON.parse(localStorage.getItem("auth")) || null;
  if (auth) {
    return auth.user;
  } else {
    return null;
  }
}


function getAccessToken() {
  const auth = JSON.parse(localStorage.getItem("auth"));
  return auth.access;
}


function getRefreshToken() {
  const auth = JSON.parse(localStorage.getItem("auth"));
  return auth.refresh;
}


function setUserData(data) {
  localStorage.setItem(
    "auth",
    JSON.stringify({
      access: data.access,
      refresh: data.refresh,
      user: data.user,
    })
  );
}

export { useUserActions, getUser, getAccessToken, getRefreshToken };