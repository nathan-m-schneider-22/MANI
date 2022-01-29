import React from "react";
import { Page, Text, Card } from "@geist-ui/react";
import { List, Home, Edit, Filter, CornerUpLeft } from "@geist-ui/react-icons";
import maniLogo from "../../assets/mani_logo.png";
import { useMediaQuery } from "react-responsive";

export default function ShortcutsPage() {
  const isLaptop = useMediaQuery({ query: "(min-width: 800px)" });

  return (
    <Page.Content
      style={{
        paddingTop: "4vh",
        paddingLeft: isLaptop ? "15vw" : "4vw",
        paddingRight: isLaptop ? "15vw" : "4vw",
        height: "90vh",
        overflow: "auto",
      }}
    >
      <Card>
        <Card.Content>
          <img
            style={{
              width: isLaptop ? "10vw" : "10vh",
              height: isLaptop ? "10vw" : "10vh",
              marginLeft: "auto",
              marginRight: "auto",
              padding: "2vw",
              backgroundColor: "pink",
              borderRadius: "3vw",
              display: "block",
            }}
            alt="logo"
            src={maniLogo}
          ></img>
          <Text>
            Welcome to <b style={{ color: "pink" }}> MANI</b>,
          </Text>
          <Text></Text>
          <Text></Text>
          <Text></Text>
          <Text></Text>
        </Card.Content>
      </Card>
    </Page.Content>
  );
}
