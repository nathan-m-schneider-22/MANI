import React from "react";
import { Page, Text, Card, Image, Link, Button } from "@geist-ui/react";
import { Power } from "@geist-ui/react-icons";
import { useHistory } from "react-router-dom";
import maniLogo from "../../assets/mani_logo.png";

export default function LandingPage() {
  const history = useHistory();
  const onClickLink = () => {
    history.push("/assistant");
  };
  return (
    <Page.Content>
      <Card margin="auto" width="400px">
        <Image src={maniLogo} height="200px" width="400px" draggable={false} />
        <center>

          <Text h2>M A N I </Text>
          <Text type="secondary" large center>
            The ASL Virtual Assistant
          </Text>
          <Button
            icon={<Power />}
            type="secondary"
            medium
            center
            onClick={onClickLink}
          >
            Preview MANI
          </Button>
        </center>
      </Card>
    </Page.Content>
  );
}
