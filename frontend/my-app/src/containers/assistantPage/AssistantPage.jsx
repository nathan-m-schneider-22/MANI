import React from "react";
import { Page, Text, Card } from "@geist-ui/react";
import { List, Home, Edit, Filter, CornerUpLeft } from "@geist-ui/react-icons";
import { useMediaQuery } from "react-responsive";

export default function AssistantPage() {
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
          <Text>
            Welcome to <b style={{ color: "pink" }}> MANI</b>! Add video stuff
            here!
          </Text>
        </Card.Content>
      </Card>
    </Page.Content>
  );
}
