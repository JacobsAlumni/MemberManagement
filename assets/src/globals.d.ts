interface Window {
    readonly jsTestModeFlag: boolean;
}

declare module "*.css" {
}

declare module "*.vue" {
    import Vue from "vue";
    export default Vue;
}