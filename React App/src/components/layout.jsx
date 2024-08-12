import React, { createContext, useMemo, useState } from "react";
import Navigationbar from "./Navbar";
import Toaster from "./Toaster";
import { useNavigate } from "react-router-dom";
import { ArrowLeftOutlined } from "@ant-design/icons";

export const Context = createContext("unknown");

function Layout(props) {
  const { hasNavigationBack } = props;
  const navigate = useNavigate();
  const [toaster, setToaster] = useState({
    title: "",
    show: false,
    message: "",
    type: "",
  });

  const value = useMemo(() => ({ toaster, setToaster }), [toaster]);

  return (
    <Context.Provider value={value}>
      <div>
        <Navigationbar />
        { hasNavigationBack && (
        <ArrowLeftOutlined
          style={{
            color: "#0D6EFD",
            fontSize: "24px",
            marginLeft: "5%",
            marginTop: "1%",
          }}
          onClick={() => navigate(-1)}
        /> )}
        <div className="container my-2">{props.children}</div>
      </div>
      <Toaster
        title={toaster.title}
        message={toaster.message}
        type={toaster.type}
        showToast={toaster.show}
        onClose={() => setToaster({ ...toaster, show: false })}
      />
    </Context.Provider>
  );
}

export default Layout;
