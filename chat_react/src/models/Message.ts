import { UserModel } from "./User.ts";

export interface MessageModel {
  id: string;
  room: string;
  from_user: UserModel;
  to_user: UserModel;
  text: string;
  timestamp: string;
  read: boolean;
}